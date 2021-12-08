import requests
from ..errors import AOCClientError
from ..typing import IAOCClient, IConfiguration


class AOCWebClient(IAOCClient):

    def get_input(self, day, year):
        return self._fetch(f"https://adventofcode.com/{year}/day/{day}/input")

    def _fetch(self, url):
        result = requests.get(url, cookies={"session": self._config.get_session_token()})
        if result.status_code == 200:
            return result.text
        raise AOCClientError("Received unsuccessfull response. %s", result.text)

    def __init__(self, config: IConfiguration):
        self._config = config
