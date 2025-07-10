from celery import Celery
import os

redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')

celery_app = Celery('workers', broker=redis_url, backend=redis_url, include=['aica_backend.workers.tasks.scraping_tasks', 'aica_backend.workers.tasks.enrichment_tasks'])

celery_app.conf.update(
    task_track_started = True,
)