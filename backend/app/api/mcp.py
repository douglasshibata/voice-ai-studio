from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import VoiceProfile, Job, ModelCatalogItem
from app.services.studio_workflows import StudioAudioWorkflows
from app.engines.registry import engine_registry

class VoiceStudioMCPServer:
    @staticmethod
    def get_tools() -> List[Dict[str, Any]]:
        return [
            {
                "name": "generate_speech",
                "description": "Synthesizes spoken audio from input text",
                "parameters": {
                    "text": "str",
                    "voice": "Optional[str]",
                    "engine": "Optional[str]",
                    "speed": "Optional[float]"
                }
            },
            {
                "name": "transcribe_audio",
                "description": "Transcribes audio/video file to text",
                "parameters": {
                    "audio_path": "str",
                    "language": "Optional[str]",
                    "diarize": "Optional[bool]"
                }
            },
            {
                "name": "list_voices",
                "description": "Lists available installed and cloned voices",
                "parameters": {}
            },
            {
                "name": "list_models",
                "description": "Lists installed AI models in the catalog",
                "parameters": {}
            },
            {
                "name": "get_job_status",
                "description": "Queries status and progress of a background job",
                "parameters": {"job_id": "str"}
            }
        ]

    @staticmethod
    def call_tool(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        if name == "generate_speech":
            return StudioAudioWorkflows.tts_synthesize(
                text=arguments.get("text", ""),
                voice_id=arguments.get("voice"),
                engine_name=arguments.get("engine", "piper"),
                speed=arguments.get("speed", 1.0)
            )
        elif name == "transcribe_audio":
            return StudioAudioWorkflows.stt_transcribe(
                audio_path=arguments.get("audio_path", ""),
                language=arguments.get("language"),
                diarize=arguments.get("diarize", False)
            )
        elif name == "list_voices":
            db = SessionLocal()
            try:
                voices = db.query(VoiceProfile).all()
                return {"voices": [{"id": v.id, "name": v.name, "is_cloned": v.is_cloned} for v in voices]}
            finally:
                db.close()
        elif name == "list_models":
            db = SessionLocal()
            try:
                models = db.query(ModelCatalogItem).all()
                return {"models": [{"id": m.id, "name": m.name, "type": m.type} for m in models]}
            finally:
                db.close()
        elif name == "get_job_status":
            db = SessionLocal()
            try:
                job = db.query(Job).filter(Job.id == arguments.get("job_id")).first()
                if not job:
                    return {"error": "Job not found"}
                return {"id": job.id, "status": job.status, "progress": job.progress, "output": job.output_files}
            finally:
                db.close()
        else:
            raise ValueError(f"Unknown MCP tool: {name}")

mcp_server = VoiceStudioMCPServer()
