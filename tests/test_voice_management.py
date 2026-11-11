import os
import wave
import unittest
from app.db.database import Base, engine, SessionLocal
from app.services.cloning_service import VoiceCloningService
from app.services.design_service import VoiceDesignService

class TestVoiceManagement(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)
        os.makedirs("./data/audio", exist_ok=True)
        cls.test_audio_path = "./data/audio/sample_voice.wav"

        with wave.open(cls.test_audio_path, "w") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(22050)
            wf.writeframesraw(b"\x00\x00" * 22050 * 3)

    def test_voice_cloning_flow(self):
        db = SessionLocal()
        try:
            profile = VoiceCloningService.clone_voice(
                db=db,
                name="Cloned Narrator",
                description="Cloned test voice",
                source_audio_path=self.test_audio_path,
                authorizer_name="John Doe",
                consent_statement="I authorize cloning my voice for studio usage.",
                gender="male",
                language="pt-BR"
            )

            self.assertTrue(profile.is_cloned)
            self.assertEqual(profile.name, "Cloned Narrator")
            self.assertIsNotNone(profile.consent_id)
            self.assertGreater(profile.quality_score, 80)
        finally:
            db.close()

    def test_voice_design_flow(self):
        db = SessionLocal()
        try:
            profile = VoiceDesignService.design_voice(
                db=db,
                name="Designed AI Host",
                prompt_description="Voz feminina brasileira, 30 anos, tom profissional e calmo",
                gender="female",
                emotion="calm",
                style="professional",
                language="pt-BR"
            )

            self.assertFalse(profile.is_cloned)
            self.assertEqual(profile.gender, "female")
            self.assertEqual(profile.acoustic_features["pitch"], 1.2)
        finally:
            db.close()

if __name__ == "__main__":
    unittest.main()
