import unittest
from app.db.database import Base, engine, SessionLocal
from app.engines.registry import engine_registry
from app.models.catalog import ModelRegistry, DEFAULT_MODELS

class TestEnginesAndCatalog(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)

    def test_engine_registry(self):
        piper = engine_registry.get_tts_engine("piper")
        self.assertIsNotNone(piper)

        result = piper.synthesize("Teste de síntese de áudio local.")
        self.assertIn("audio_path", result)
        self.assertGreater(result["duration_seconds"], 0)

        whisper = engine_registry.get_asr_engine("faster-whisper")
        self.assertIsNotNone(whisper)

        transcription = whisper.transcribe("dummy.wav", diarize=True)
        self.assertIn("segments", transcription)
        self.assertGreater(len(transcription["segments"]), 0)

    def test_model_catalog(self):
        db = SessionLocal()
        try:
            ModelRegistry.seed_defaults(db)
            models = ModelRegistry.list_models(db)
            self.assertGreaterEqual(len(models), len(DEFAULT_MODELS))

            tts_models = ModelRegistry.list_models(db, model_type="tts")
            self.assertTrue(any(m.id == "piper-pt-br-faber-medium" for m in tts_models))
        finally:
            db.close()

if __name__ == "__main__":
    unittest.main()
