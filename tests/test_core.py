import unittest
from app.db.database import Base, engine, SessionLocal
from app.db.models import VoiceProfile, Job, ModelCatalogItem
from app.core.hardware import HardwareDetector
from app.core.memory_manager import memory_manager

class TestCoreInfrastructure(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)

    def test_database_models(self):
        db = SessionLocal()
        try:
            profile = VoiceProfile(name="Test Voice", language="pt-BR")
            db.add(profile)
            db.commit()
            db.refresh(profile)

            self.assertIsNotNone(profile.id)
            self.assertEqual(profile.name, "Test Voice")

            job = Job(type="tts", status="queued")
            db.add(job)
            db.commit()
            db.refresh(job)

            self.assertIsNotNone(job.id)
            self.assertEqual(job.status, "queued")
        finally:
            db.close()

    def test_hardware_detector(self):
        hw = HardwareDetector.detect()
        self.assertIn("device", hw)
        self.assertIn("system", hw)
        self.assertIn("ram_gb", hw["system"])

    def test_memory_manager(self):
        dummy_load = lambda: "dummy_model_instance"
        model = memory_manager.load_model("test_model", dummy_load, vram_gb=0.5)
        self.assertEqual(model, "dummy_model_instance")
        info = memory_manager.get_loaded_info()
        self.assertIn("test_model", info)
        memory_manager.unload_model("test_model")
        self.assertNotIn("test_model", memory_manager.get_loaded_info())

if __name__ == "__main__":
    unittest.main()
