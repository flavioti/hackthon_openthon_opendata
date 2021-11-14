import json
from datetime import datetime
from time import sleep

import amazon.ion.simpleion as ion
from pyion2json import ion_cursor_to_json
from pyqldb.config.retry_config import RetryConfig
from pyqldb.driver.qldb_driver import QldbDriver

from .celery_app import celery_app
from .resolvrisk import ResolvRiskClient

# Configure retry limit to 3
retry_config = RetryConfig(retry_limit=3)

# Initialize the driver
print("Initializing the driver")
qldb_driver = QldbDriver("dataftwdb", retry_config=retry_config)

# TODO: Implementar modelo v1
# TODO: Executar modelo v1 com base nas variáveis de da resolvrisk e SPC


@celery_app.task(
    rate_limit="10/m",
)
def consulta_credito_task(cpf):

    # Consulta API da ResolvRisk
    rrc = ResolvRiskClient()
    api_response = json.loads(rrc.consulta_credito(cpf, 12))

    if api_response["statusCode"] != 200:
        return f"{api_response['statusCode']} {api_response['message']}"

    api_response["data"]["dt_consulta"] = datetime.now().isoformat()

    # Simula consulta ao SPC
    api_response["data"]["score"] = qldb_driver.execute_lambda(
        lambda executor: consulta_clientes_pf(
            executor,
            cpf,
        )
    )

    api_response["data"]["modificador"] = qldb_driver.execute_lambda(
        lambda executor: consulta_empregabilidade(
            executor,
            api_response["data"]["nivelEmpregabilidade"],
        )
    )

    #  Grava dados do cliente na tabela
    qldb_driver.execute_lambda(
        lambda executor: write_response(executor, api_response["data"])
    )

    return api_response["data"]


def write_response(transaction_executor, dados_cliente: dict):
    """
    Grava dados obtidos da API da ResolvRisk
    """
    transaction_executor.execute_statement(
        f"INSERT INTO Consultas_Cliente_PF {dados_cliente}"
    )


def consulta_clientes_pf(transaction_executor, cpf: str) -> str:
    cursor = transaction_executor.execute_statement(
        "SELECT * FROM Clientes_PF WHERE CPF = ?", cpf
    )

    for doc in cursor:
        return doc["SCORE"]


def consulta_empregabilidade(transaction_executor, range: int) -> int:
    cursor = transaction_executor.execute_statement(
        "SELECT modificador FROM Scores_Empregabilidade WHERE ? BETWEEN inicio AND fim",
        range,
    )

    for doc in cursor:
        return doc["modificador"]


def consulta_dados_clientes(transaction_executor, cpf: str) -> str:
    cursor = transaction_executor.execute_statement(
        "SELECT * FROM Clientes_PF WHERE CPF = ?", cpf
    )

    for doc in cursor:
        return ion.dumps(doc, binary=False)


@celery_app.task(
    rate_limit="10/m",
)
def consulta_dados_cliente_task(cpf):
    sleep(1)
    r = qldb_driver.execute_lambda(
        lambda executor: consulta_dados_clientes(executor, cpf)
    )
    return r
