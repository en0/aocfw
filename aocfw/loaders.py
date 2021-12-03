from typing import Callable, IO

from .typing import ILoader


class FileLoader(ILoader):
    def read(self, callback: Callable[[IO], any], **kwargs) -> any:
        with open(kwargs.get("source"), kwargs.get("mode", "r")) as fd:
            return callback(fd)

