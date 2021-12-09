import logging
from argparse import ArgumentParser, Namespace
from typing import List, Type
from pyioc3 import StaticContainerBuilder

from .typing import IEntryPoint
from ..typing import IConfiguration, IAOCClient

from ..client import AOCWebClient
from ..config import IniConfiguration


class EntryPoint:

    def add(self, entry_point: Type[IEntryPoint]):
        self._ioc_builder.bind(entry_point, entry_point)
        self._entry_points.append(entry_point)

    def get_opts(self):
        ap = ArgumentParser()
        ap.add_argument('--config', default=".aocfwrc", type=str, help="Change configuration file")
        ap.add_argument('--log-level', default="INFO", type=str, help="Set the log level.")
        sp = ap.add_subparsers(help='sub-command help')

        for entry_point in self._entry_points:
            _ap = entry_point.argdef(sp)
            _ap.set_defaults(_entry_point=entry_point)

        return ap.parse_args()

    def configure(self, opts: Namespace):
        self._ioc_builder.bind_constant(Namespace, opts)
        self._ioc_builder.bind(IConfiguration, IniConfiguration)
        self._ioc_builder.bind(IAOCClient, AOCWebClient)

    def run(self):
        opts = self.get_opts()
        logging.basicConfig(
            format='[%(levelname)s]\t%(message)s',
            level=opts.log_level
        )

        if not opts._entry_point:
            logging.error("No command! try --help")
            return 1

        try:
            self.configure(opts)
            result = self._ioc_builder.build().get(opts._entry_point).run()

        except:
            logging.exception("Unexpcted error!")
            result = 1

        finally:
            return 0 if result is None else result

    def __init__(self):
        self._ioc_builder = StaticContainerBuilder()
        self._entry_points: List[Type[IEntryPoint]] = []


def main():

    from .create_config import CreateConfigEntryPoint
    from .create_day import CreateDayEntryPoint
    from .download_input import DownloadInputEntryPoint
    from .submit_answer import SubmitAnswerEntryPoint
    from .run_solution import RunSolutionEntryPoint

    ep = EntryPoint()
    ep.add(CreateConfigEntryPoint)
    ep.add(CreateDayEntryPoint)
    ep.add(DownloadInputEntryPoint)
    ep.add(SubmitAnswerEntryPoint)
    ep.add(RunSolutionEntryPoint)
    return ep.run()

