from celery import Celery
from celery.schedules import crontab

from ..core.config import settings
from .tasks.scraping_tasks import trigger_daily_scraping

celery_app = Celery(
    "workers",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=[
        "aica_backend.workers.tasks.scraping_tasks",
        "aica_backend.workers.tasks.enrichment_tasks",
        "aica_backend.workers.tasks.embedding_tasks",
        "aica_backend.workers.tasks.pipeline_tasks",
        "aica_backend.workers.tasks.monitoring_tasks"
    ]
)

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=8, minute=0),
        trigger_daily_scraping.s(),
        name='Run daily job scraping pipeline'
    )