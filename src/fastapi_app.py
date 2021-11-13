import logging

from fastapi import BackgroundTasks, FastAPI

from .worker import celery_app

app = FastAPI()

log = logging.getLogger(__name__)


def background_on_message(task):
    # log.warn(task.get(propagate=False))
    pass


@app.get("/")
async def ping(background_task: BackgroundTasks):
    task_name = "src.worker.test_celery"
    task = celery_app.send_task(task_name, args=[])
    background_task.add_task(background_on_message, task)

    return {"message": "ok"}
