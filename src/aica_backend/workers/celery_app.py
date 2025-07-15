from celery import Celery
from celery.schedules import crontab

from ..core.config import settings

celery_app = Celery(
    "workers",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["aica_backend.workers.tasks.data_pipeline_tasks"]
)

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=8, minute=0),
        # run_full_job_pipeline.s(),
        name='Run daily job scraping pipeline'
    )