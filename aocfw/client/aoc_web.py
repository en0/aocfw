import requests
from bs4 import BeautifulSoup
from ..errors import AOCClientError
from ..typing import IAOCClient, IConfiguration


class AOCWebClient(IAOCClient):

    def get_input(self, day: int, year: int) -> str:
        return self._get(f"https://adventofcode.com/{year}/day/{day}/input")

    def submit_answer(self, day: int, year: int, part: int, value: any) -> str:
        result = self._post(f'https://adventofcode.com/{year}/day/{day}/answer', {
            "level": part,
            "answer": value,
        })
        soup = BeautifulSoup(result, features="html.parser")
        return soup.find("article").text

    def _get(self, url):
        result = requests.get(url, cookies={"session": self._config.get_session_token()})
        if result.status_code == 200:
            return result.text
        raise AOCClientError(f"Received unsuccessful response.\n{result.text}")

    def _post(self, url: str, data: dict):
        result = requests.post(
            url=url,
            cookies={"session": self._config.get_session_token()},
            headers={"content-type": "application/x-www-form-urlencoded"},
            data=data)
        if 300 > result.status_code >= 200:
            return result.text
        raise AOCClientError(f"Received unsuccessful response.\n{result.text}")

    def __init__(self, config: IConfiguration):
        self._config = config
