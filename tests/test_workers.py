import unittest
from app.db.database import Base, engine, SessionLocal
from app.db.models import Job
from app.workers.job_runner import JobRunner

class TestJobWorkerSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)

    def test_job_execution_lifecycle(self):
        db = SessionLocal()
        try:
            job = Job(type="tts", status="queued", input_params={"text": "Test Job"})
            db.add(job)
            db.commit()
            db.refresh(job)

            def mock_handler(params, progress_cb):
                progress_cb(50.0)
                return {"audio_path": "./data/audio/job_output.wav"}

            JobRunner.execute_job(db, job.id, mock_handler)

            updated_job = db.query(Job).filter(Job.id == job.id).first()
            self.assertEqual(updated_job.status, "completed")
            self.assertEqual(updated_job.progress, 100.0)
            self.assertIn("audio_path", updated_job.output_files)
        finally:
            db.close()

if __name__ == "__main__":
    unittest.main()
