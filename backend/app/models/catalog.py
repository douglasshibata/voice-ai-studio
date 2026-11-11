import logging
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.db.models import ModelCatalogItem

logger = logging.getLogger("voice_ai_studio.models.catalog")

DEFAULT_MODELS = [
    {
        "id": "piper-pt-br-faber-medium",
        "name": "Piper Faber Medium (pt-BR)",
        "engine": "piper",
        "type": "tts",
        "languages": ["pt-BR"],
        "voice_cloning": False,
        "voice_design": False,
        "streaming": True,
        "size_mb": 65.0,
        "vram_required_gb": 0.5,
        "cpu_compatible": True,
        "gpu_compatible": True,
        "license_name": "MIT",
        "commercial_allowed": True,
        "installed": True,
        "is_default": True
    },
    {
        "id": "faster-whisper-medium",
        "name": "Faster-Whisper Medium (Multilingual)",
        "engine": "faster-whisper",
        "type": "asr",
        "languages": ["pt-BR", "en-US", "es-ES", "fr-FR"],
        "voice_cloning": False,
        "voice_design": False,
        "streaming": False,
        "size_mb": 1500.0,
        "vram_required_gb": 2.0,
        "cpu_compatible": True,
        "gpu_compatible": True,
        "license_name": "MIT",
        "commercial_allowed": True,
        "installed": True,
        "is_default": True
    },
    {
        "id": "demucs-htdemucs",
        "name": "Demucs Stem Separator",
        "engine": "ffmpeg-demucs",
        "type": "audio_proc",
        "languages": [],
        "voice_cloning": False,
        "voice_design": False,
        "streaming": False,
        "size_mb": 80.0,
        "vram_required_gb": 1.0,
        "cpu_compatible": True,
        "gpu_compatible": True,
        "license_name": "MIT",
        "commercial_allowed": True,
        "installed": True,
        "is_default": True
    }
]

class ModelRegistry:
    @staticmethod
    def seed_defaults(db: Session):
        for item in DEFAULT_MODELS:
            existing = db.query(ModelCatalogItem).filter(ModelCatalogItem.id == item["id"]).first()
            if not existing:
                catalog_item = ModelCatalogItem(**item)
                db.add(catalog_item)
        db.commit()

    @staticmethod
    def list_models(db: Session, engine: Optional[str] = None, model_type: Optional[str] = None) -> List[ModelCatalogItem]:
        query = db.query(ModelCatalogItem)
        if engine:
            query = query.filter(ModelCatalogItem.engine == engine)
        if model_type:
            query = query.filter(ModelCatalogItem.type == model_type)
        return query.all()

    @staticmethod
    def set_installed(db: Session, model_id: str, installed: bool):
        model = db.query(ModelCatalogItem).filter(ModelCatalogItem.id == model_id).first()
        if model:
            model.installed = installed
            db.commit()

    @staticmethod
    def set_default(db: Session, model_id: str):
        model = db.query(ModelCatalogItem).filter(ModelCatalogItem.id == model_id).first()
        if model:
            db.query(ModelCatalogItem).filter(ModelCatalogItem.type == model.type).update({"is_default": False})
            model.is_default = True
            db.commit()
