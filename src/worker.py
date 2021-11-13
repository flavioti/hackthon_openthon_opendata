from .celery_app import celery_app
from datetime import datetime


@celery_app.task(
    rate_limit="5/m",
)
def test_celery():
    print(datetime.now())
