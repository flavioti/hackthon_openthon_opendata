import os

import requests


class ResolvRiskClient:
    def __init__(self) -> None:

        self.url = os.environ.get("URL")
        self.token = os.environ.get("TOKEN")

    def __do_request(self, endpoint: str, data: dict):
        r = requests.post(
            f"{self.url}{endpoint}",
            headers={
                "Authorization": self.token,
            },
            json=data,
        )
        return r

    def consulta_credito(self, cpf: str, tempo: int = 12):
        r = self.__do_request(
            "/credito",
            data={
                "cpf": cpf,
                "tempo": tempo,
            },
        )

        return r.content.decode("utf-8")
