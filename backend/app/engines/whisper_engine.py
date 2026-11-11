import os
import logging
from typing import Optional, Dict, Any
from app.engines.base import ASREngine

logger = logging.getLogger("voice_ai_studio.engines.whisper")

class FasterWhisperASREngine(ASREngine):
    name = "faster-whisper"
    capabilities = ["asr", "timestamps", "diarization"]
    languages = ["pt-BR", "en-US", "es-ES", "fr-FR", "de-DE"]

    def __init__(self):
        self.loaded = False
        self.current_model = None

    def is_available(self) -> bool:
        return True

    def load_model(self, model_id: Optional[str] = None):
        self.current_model = model_id or "whisper-medium"
        self.loaded = True
        logger.info(f"Loaded Faster-Whisper model: {self.current_model}")

    def unload_model(self):
        self.loaded = False
        self.current_model = None

    def transcribe(
        self,
        audio_path: str,
        language: Optional[str] = None,
        diarize: bool = False,
        settings: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        if not self.loaded:
            self.load_model()

        detected_language = language or "pt-BR"

        # Robust mock transcription extraction
        segments = [
            {
                "start": 0.0,
                "end": 2.5,
                "speaker": "Speaker 1" if diarize else None,
                "text": "Olá, seja bem-vindo ao Voice AI Studio."
            },
            {
                "start": 2.8,
                "end": 5.5,
                "speaker": "Speaker 2" if diarize else None,
                "text": "Esta é uma transcrição local de alta fidelidade e baixa latência."
            }
        ]

        full_text = " ".join([seg["text"] for seg in segments])

        return {
            "text": full_text,
            "language": detected_language,
            "segments": segments,
            "audio_path": audio_path
        }
