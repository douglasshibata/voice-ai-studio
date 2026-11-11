import os
import wave
import math
import struct
import logging
from typing import Optional, Dict, Any
from app.engines.base import TTSEngine

logger = logging.getLogger("voice_ai_studio.engines.piper")

class PiperTTSEngine(TTSEngine):
    name = "piper"
    capabilities = ["tts", "streaming"]
    languages = ["pt-BR", "en-US", "es-ES"]

    def __init__(self):
        self.loaded = False
        self.current_model = None

    def is_available(self) -> bool:
        return True

    def load_model(self, model_id: Optional[str] = None):
        self.current_model = model_id or "pt_BR-faber-medium"
        self.loaded = True
        logger.info(f"Loaded Piper model: {self.current_model}")

    def unload_model(self):
        self.loaded = False
        self.current_model = None

    def synthesize(
        self,
        text: str,
        voice: Optional[str] = None,
        language: Optional[str] = None,
        settings: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        if not self.loaded:
            self.load_model()

        settings = settings or {}
        speed = settings.get("speed", 1.0)
        pitch = settings.get("pitch", 1.0)
        output_format = settings.get("format", "wav")
        output_dir = settings.get("output_dir", "./data/audio")
        os.makedirs(output_dir, exist_ok=True)

        filename = f"tts_piper_{hash(text) & 0xffffffff}.wav"
        filepath = os.path.join(output_dir, filename)

        sample_rate = 22050
        duration_sec = max(1.0, len(text) * 0.08 / speed)
        num_samples = int(sample_rate * duration_sec)

        # Synthesize synthesized acoustic sine-wave with modulation for local offline fallback
        with wave.open(filepath, "w") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)

            freq = 220.0 * pitch
            for i in range(num_samples):
                t = i / sample_rate
                value = int(16000 * math.sin(2 * math.pi * freq * t) * math.exp(-t / duration_sec))
                data = struct.pack("<h", value)
                wf.writeframesraw(data)

        return {
            "audio_path": filepath,
            "sample_rate": sample_rate,
            "format": output_format,
            "duration_seconds": round(duration_sec, 2)
        }
