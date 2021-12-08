from configparser import ConfigParser
from argparse import Namespace

from .typing import IConfiguration


class IniConfiguration(IConfiguration):

    def new(self, path: str) -> None:
        self._path = path
        self._config = ConfigParser()

    def get_session_token(self) -> str:
        return self.config.get("creds", "token")

    def set_session_token(self, value: str) -> None:
        self._ensure_section("creds")
        self.config.set("creds", "token", value)
        self.save()

    def get_year(self) -> int:
        return self.config.get("calendar", "year")

    def set_year(self, value: int) -> None:
        self._ensure_section("calendar")
        self.config.set("calendar", "year", value)
        self.save()

    @property
    def config(self) -> ConfigParser:
        if self._config is None:
            self._config = ConfigParser()
            self._config.read(self._path)
        return self._config

    def save(self) -> None:
        with open(self._path, "w") as fd:
            self.config.write(fd)

    def _ensure_section(self, section: str) -> None:
        if not self.config.has_section(section):
            self.config.add_section(section)

    def __init__(self, opts: Namespace):
        self._path = opts.config
        self._config = None
