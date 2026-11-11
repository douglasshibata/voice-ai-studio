import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, Float, Integer, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class VoiceProfile(Base):
    __tablename__ = "voice_profiles"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    gender = Column(String, nullable=True)
    language = Column(String, default="pt-BR")
    created_at = Column(DateTime, default=datetime.utcnow)

    is_cloned = Column(Boolean, default=False)
    source_audio_path = Column(String, nullable=True)
    audio_duration_seconds = Column(Float, nullable=True)
    sample_rate = Column(Integer, nullable=True)
    snr_db = Column(Float, nullable=True)
    quality_score = Column(Float, nullable=True)

    acoustic_features = Column(JSON, nullable=True) # Pitch, rate, energy, emotion
    embedding_path = Column(String, nullable=True)
    consent_id = Column(String, ForeignKey("user_consents.id"), nullable=True)

class ModelCatalogItem(Base):
    __tablename__ = "model_catalog_items"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    engine = Column(String, nullable=False) # e.g., piper, coqui, faster-whisper
    type = Column(String, nullable=False) # tts, asr, voice_conversion, audio_proc
    languages = Column(JSON, default=list)

    voice_cloning = Column(Boolean, default=False)
    voice_design = Column(Boolean, default=False)
    streaming = Column(Boolean, default=False)

    size_mb = Column(Float, default=0.0)
    vram_required_gb = Column(Float, default=0.0)
    cpu_compatible = Column(Boolean, default=True)
    gpu_compatible = Column(Boolean, default=True)

    license_name = Column(String, nullable=False)
    commercial_allowed = Column(Boolean, default=True)
    source_url = Column(String, nullable=True)

    installed = Column(Boolean, default=False)
    local_path = Column(String, nullable=True)
    is_default = Column(Boolean, default=False)

class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    type = Column(String, nullable=False) # tts, stt, clone, dubbing, audiobook
    status = Column(String, default="queued") # queued, processing, completed, failed, cancelled, paused
    progress = Column(Float, default=0.0)

    input_params = Column(JSON, nullable=True)
    output_files = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)
    logs = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

class Project(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    type = Column(String, default="dubbing") # dubbing, audiobook, studio

    state_data = Column(JSON, nullable=True) # Timeline, transcripts, voice mappings
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class UserConsent(Base):
    __tablename__ = "user_consents"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    voice_name = Column(String, nullable=False)
    authorizer_name = Column(String, nullable=False)
    statement = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
