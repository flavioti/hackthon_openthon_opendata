import logging

from fastapi import BackgroundTasks, FastAPI

from .worker import celery_app

fastapi_app = FastAPI()

log = logging.getLogger(__name__)


def background_on_message(task):
    pass


@fastapi_app.get("/")
async def ping(background_task: BackgroundTasks):
    task = celery_app.send_task(
        "src.worker.test_celery",
        args=[],
    )
    background_task.add_task(background_on_message, task)

    return {"message": "ok"}


# http://127.0.0.1:8000/consultar_credito?cpf=xxxxxxxxxxx
@fastapi_app.get("/consultar_credito")
async def consultar_credito(cpf: str, background_task: BackgroundTasks):
    task = celery_app.send_task(
        "src.worker.consulta_credito_task",
        args=[cpf],
    )
    background_task.add_task(background_on_message, task)

    return {"message": "ok"}
