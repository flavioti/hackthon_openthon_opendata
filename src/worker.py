from pyqldb.config.retry_config import RetryConfig
from pyqldb.driver.qldb_driver import QldbDriver
from .celery_app import celery_app
from datetime import datetime
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
@celery_app.task()
def consulta_credito_task(cpf):
    print("Consultando credito")
    rrc = ResolvRiskClient()
    r = rrc.consulta_credito(cpf, 12)
    print(r)


@celery_app.task(
    rate_limit="10/m",
)
def consulta_credito_task():
    print(datetime.now())
    # Query the table
    qldb_driver.execute_lambda(lambda executor: read_documents(executor))


def read_documents(transaction_executor):
    print("Querying the table")
    cursor = transaction_executor.execute_statement(
        "SELECT * FROM People WHERE lastName = ?", "Doe"
    )

    for doc in cursor:
        print(doc["firstName"])
        print(doc["lastName"])
        print(doc["age"])
