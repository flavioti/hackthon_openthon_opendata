import json
import logging

from fastapi import BackgroundTasks, FastAPI, Response

from .worker import celery_app

fastapi_app = FastAPI()

log = logging.getLogger(__name__)


def background_on_message(task):
    pass


# http://127.0.0.1:8000/consultar_credito?cpf=xxxxxxxxxxx
@fastapi_app.get("/consultar_credito")
async def consultar_credito(cpf: str, background_task: BackgroundTasks):
    task = celery_app.send_task(
        "src.worker.consulta_credito_task",
        args=[cpf],
    )
    background_task.add_task(background_on_message, task)

    return Response(content=json.dumps({"status": "ok"}), status_code=200)


@fastapi_app.get("/healthcheck")
async def healthcheck():
    return Response(content=json.dumps({"status": "ok"}), status_code=200)


@fastapi_app.get("/consultadados")
async def consulta_dados(cpf: str, background_task: BackgroundTasks):
    task = celery_app.send_task(
        "src.worker.consulta_dados_cliente_task",
        args=[cpf],
    )
    result = task.wait(timeout=10, interval=0.5)

    return Response(content=json.dumps(result), status_code=200)
