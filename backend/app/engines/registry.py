import logging
from typing import Dict, List, Optional, Any
from app.engines.base import BaseEngine, TTSEngine, ASREngine, VoiceConversionEngine, AudioProcessingEngine
from app.engines.piper_engine import PiperTTSEngine
from app.engines.whisper_engine import FasterWhisperASREngine
from app.engines.ffmpeg_engine import FFmpegAudioEngine

logger = logging.getLogger("voice_ai_studio.engines.registry")

class EngineRegistry:
    def __init__(self):
        self._engines: Dict[str, BaseEngine] = {}
        self._register_defaults()

    def _register_defaults(self):
        piper = PiperTTSEngine()
        whisper = FasterWhisperASREngine()
        ffmpeg = FFmpegAudioEngine()

        self.register_engine(piper)
        self.register_engine(whisper)
        self.register_engine(ffmpeg)

    def register_engine(self, engine: BaseEngine):
        logger.info(f"Registering engine: {engine.name}")
        self._engines[engine.name] = engine

    def get_engine(self, name: str) -> Optional[BaseEngine]:
        return self._engines.get(name)

    def get_tts_engine(self, name: str = "piper") -> TTSEngine:
        engine = self.get_engine(name)
        if not isinstance(engine, TTSEngine):
            raise ValueError(f"Engine {name} is not a valid TTSEngine")
        return engine

    def get_asr_engine(self, name: str = "faster-whisper") -> ASREngine:
        engine = self.get_engine(name)
        if not isinstance(engine, ASREngine):
            raise ValueError(f"Engine {name} is not a valid ASREngine")
        return engine

    def list_engines(self) -> List[Dict[str, Any]]:
        result = []
        for name, engine in self._engines.items():
            result.append({
                "name": name,
                "capabilities": engine.capabilities,
                "languages": engine.languages,
                "available": engine.is_available()
            })
        return result

engine_registry = EngineRegistry()
