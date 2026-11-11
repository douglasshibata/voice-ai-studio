from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class BaseEngine(ABC):
    name: str
    capabilities: List[str]
    languages: List[str]

    @abstractmethod
    def is_available(self) -> bool:
        pass

    @abstractmethod
    def load_model(self, model_id: Optional[str] = None):
        pass

    @abstractmethod
    def unload_model(self):
        pass

class TTSEngine(BaseEngine, ABC):
    @abstractmethod
    def synthesize(
        self,
        text: str,
        voice: Optional[str] = None,
        language: Optional[str] = None,
        settings: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Returns dict with audio_path, sample_rate, format, duration."""
        pass

class ASREngine(BaseEngine, ABC):
    @abstractmethod
    def transcribe(
        self,
        audio_path: str,
        language: Optional[str] = None,
        diarize: bool = False,
        settings: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Returns dict with text, segments (timestamps, speaker, text), language."""
        pass

class VoiceConversionEngine(BaseEngine, ABC):
    @abstractmethod
    def convert(
        self,
        source_audio_path: str,
        target_voice: str,
        settings: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Returns dict with converted audio_path."""
        pass

class AudioProcessingEngine(BaseEngine, ABC):
    @abstractmethod
    def process_audio(
        self,
        audio_path: str,
        action: str, # noise_reduction, stem_separation, silence_removal
        settings: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Returns dict with processed audio_path, metrics."""
        pass
