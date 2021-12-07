from typing import Callable, IO

from .typing import ILoader


class AutoLoader(ILoader):

    def read(self, callback: Callable[[IO], any], **kwargs) -> any:
        if "sample" in kwargs:
            return self.read_sample(callback, **kwargs)

        elif "source" in kwargs:
            return self.read_file(callback, **kwargs)

        else:
            raise RuntimeError('No input data provided. Use keyward "source" or "sample"')

    def read_sample(self, callback: Callable[[IO], any], **kwargs) -> any:
        return callback(kwargs["sample"])

    def read_file(self, callback: Callable[[IO], any], **kwargs) -> any:
        with open(kwargs["source"], kwargs.get("mode", "r")) as fd:
            return callback(fd)

