from celery import Celery
import os

celery_app = Celery("resolvrisk_bureau")
celery_app.conf.broker_url = os.environ.get("BROKER_URL")
celery_app.conf.task_track_started = True

celery_app.autodiscover_tasks(["src.worker"])
