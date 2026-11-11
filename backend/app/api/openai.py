import os
from typing import Optional
from fastapi import APIRouter, HTTPException, Form, UploadFile, File
from fastapi.responses import FileResponse
from app.services.studio_workflows import StudioAudioWorkflows

openai_router = APIRouter(prefix="/v1")

@openai_router.post("/audio/speech")
def openai_speech(payload: dict):
    input_text = payload.get("input")
    voice = payload.get("voice", "alloy")
    response_format = payload.get("response_format", "mp3")
    speed = payload.get("speed", 1.0)

    if not input_text:
        raise HTTPException(status_code=400, detail="Field 'input' is required.")

    res = StudioAudioWorkflows.tts_synthesize(
        text=input_text,
        voice_id=voice,
        speed=speed,
        output_format=response_format
    )

    audio_path = res["audio_path"]
    if os.path.exists(audio_path):
        return FileResponse(path=audio_path, media_type=f"audio/{response_format}")
    return res

@openai_router.post("/audio/transcriptions")
def openai_transcribe(
    file: UploadFile = File(...),
    model: str = Form("whisper-1"),
    language: Optional[str] = Form(None)
):
    upload_dir = "./data/audio"
    os.makedirs(upload_dir, exist_ok=True)
    temp_path = os.path.join(upload_dir, f"openai_in_{file.filename}")

    with open(temp_path, "wb") as buffer:
        buffer.write(file.file.read())

    res = StudioAudioWorkflows.stt_transcribe(
        audio_path=temp_path,
        language=language
    )
    return {"text": res["text"]}
