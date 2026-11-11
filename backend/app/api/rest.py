import os
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import VoiceProfile, Job, ModelCatalogItem, Project
from app.core.hardware import HardwareDetector
from app.core.memory_manager import memory_manager
from app.engines.registry import engine_registry
from app.models.catalog import ModelRegistry
from app.services.cloning_service import VoiceCloningService
from app.services.design_service import VoiceDesignService
from app.services.studio_workflows import StudioAudioWorkflows
from app.workers.job_runner import JobRunner

router = APIRouter(prefix="/api/v1")

@router.get("/hardware")
def get_hardware_status():
    return HardwareDetector.detect()

@router.get("/memory")
def get_memory_status():
    return memory_manager.get_loaded_info()

@router.get("/engines")
def list_engines():
    return engine_registry.list_engines()

@router.get("/models")
def list_models(db: Session = Depends(get_db)):
    return ModelRegistry.list_models(db)

@router.post("/tts")
def tts_generate(payload: Dict[str, Any]):
    text = payload.get("text")
    if not text:
        raise HTTPException(status_code=400, detail="Field 'text' is required.")

    engine_name = payload.get("engine", "piper")
    voice = payload.get("voice")
    language = payload.get("language", "pt-BR")
    speed = payload.get("speed", 1.0)
    pitch = payload.get("pitch", 1.0)

    res = StudioAudioWorkflows.tts_synthesize(
        text=text, voice_id=voice, engine_name=engine_name,
        language=language, speed=speed, pitch=pitch
    )
    return res

@router.post("/transcribe")
def transcribe_audio(payload: Dict[str, Any]):
    audio_path = payload.get("audio_path")
    if not audio_path or not os.path.exists(audio_path):
        raise HTTPException(status_code=400, detail="Valid 'audio_path' is required.")

    engine_name = payload.get("engine", "faster-whisper")
    language = payload.get("language")
    diarize = payload.get("diarize", False)

    return StudioAudioWorkflows.stt_transcribe(
        audio_path=audio_path, engine_name=engine_name, language=language, diarize=diarize
    )

@router.get("/voices")
def list_voices(db: Session = Depends(get_db)):
    return db.query(VoiceProfile).all()

@router.post("/voices/clone")
def clone_voice(
    name: str = Form(...),
    description: str = Form(...),
    authorizer_name: str = Form(...),
    consent_statement: str = Form(...),
    gender: Optional[str] = Form("unspecified"),
    language: Optional[str] = Form("pt-BR"),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    upload_dir = "./data/audio"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, f"source_{file.filename}")

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    profile = VoiceCloningService.clone_voice(
        db=db, name=name, description=description, source_audio_path=file_path,
        authorizer_name=authorizer_name, consent_statement=consent_statement,
        gender=gender, language=language
    )
    return profile

@router.post("/voices/design")
def design_voice(payload: Dict[str, Any], db: Session = Depends(get_db)):
    name = payload.get("name")
    prompt_description = payload.get("prompt_description")
    if not name or not prompt_description:
        raise HTTPException(status_code=400, detail="'name' and 'prompt_description' are required.")

    profile = VoiceDesignService.design_voice(
        db=db, name=name, prompt_description=prompt_description,
        gender=payload.get("gender", "female"),
        emotion=payload.get("emotion", "calm"),
        style=payload.get("style", "professional"),
        language=payload.get("language", "pt-BR")
    )
    return profile

@router.post("/jobs")
def create_job(payload: Dict[str, Any], background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    job_type = payload.get("type")
    params = payload.get("params", {})
    if not job_type:
        raise HTTPException(status_code=400, detail="Field 'type' is required.")

    job = Job(type=job_type, status="queued", input_params=params)
    db.add(job)
    db.commit()
    db.refresh(job)

    def job_handler(job_id, job_type, params):
        def exec_fn(inp, cb):
            if job_type == "tts":
                cb(30.0)
                res = StudioAudioWorkflows.tts_synthesize(text=inp.get("text", "Default text"))
                cb(90.0)
                return res
            elif job_type == "dubbing":
                cb(20.0)
                res = StudioAudioWorkflows.video_dubbing_pipeline(video_path=inp.get("video_path", "sample.mp4"))
                cb(90.0)
                return res
            elif job_type == "audiobook":
                cb(20.0)
                res = StudioAudioWorkflows.audiobook_studio_process(
                    document_text=inp.get("text", ""),
                    chapters=inp.get("chapters", []),
                    character_voice_map=inp.get("voice_map", {})
                )
                cb(90.0)
                return res
            return {"status": "ok"}

        with Session(get_db().bind) as sess:
            JobRunner.execute_job(sess, job_id, exec_fn)

    background_tasks.add_task(job_handler, job.id, job_type, params)
    return job

@router.get("/jobs")
def list_jobs(db: Session = Depends(get_db)):
    return db.query(Job).order_by(Job.created_at.desc()).all()

@router.get("/jobs/{job_id}")
def get_job(job_id: str, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")
    return job
