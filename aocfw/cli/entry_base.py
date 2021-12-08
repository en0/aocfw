from pyioc3 import StaticContainerBuilder
from logging import Logger, getLogger
from argparse import Namespace

from .typing import IEntryPoint
from ..typing import IConfiguration, IAOCClient


class EntryPointBase(IEntryPoint):

    @property
    def opts(self) -> Namespace:
        return self._opts

    @property
    def config(self) -> IConfiguration:
        return self._config

    @property
    def log(self) -> Logger:
        if self._log is None:
            self._log = getLogger(self.__class__.__name__)
        return self._log

    @property
    def aoc_client(self) -> IAOCClient:
        return self._aoc_client

    def __init__(self, opts: Namespace, config: IConfiguration, aoc_client: IAOCClient):
        self._opts = opts
        self._config = config
        self._aoc_client = aoc_client
        self._log = None
