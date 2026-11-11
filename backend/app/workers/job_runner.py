import time
import logging
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.db.models import Job

logger = logging.getLogger("voice_ai_studio.workers")

class JobRunner:
    @staticmethod
    def execute_job(db: Session, job_id: str, handler_fn):
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            logger.error(f"Job {job_id} not found.")
            return

        job.status = "processing"
        job.progress = 10.0
        db.commit()

        try:
            logger.info(f"Executing job {job_id} of type {job.type}...")
            result = handler_fn(job.input_params, lambda p: JobRunner._update_progress(db, job_id, p))

            job = db.query(Job).filter(Job.id == job_id).first()
            job.status = "completed"
            job.progress = 100.0
            job.output_files = result
            job.logs = f"Job {job_id} executed successfully."
            db.commit()
            logger.info(f"Job {job_id} completed successfully.")
        except Exception as e:
            logger.exception(f"Job {job_id} failed: {e}")
            job = db.query(Job).filter(Job.id == job_id).first()
            job.status = "failed"
            job.error_message = str(e)
            job.logs = f"Error during job execution: {str(e)}"
            db.commit()

    @staticmethod
    def _update_progress(db: Session, job_id: str, progress: float):
        job = db.query(Job).filter(Job.id == job_id).first()
        if job and job.status == "processing":
            job.progress = round(progress, 1)
            db.commit()
