from celery import Celery
import os

app = Celery("resolvrisk_bureau")
app.conf.broker_url = os.environ.get("BROKER_URL")
