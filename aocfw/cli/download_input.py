from argparse import _SubParsersAction, ArgumentParser
from datetime import datetime
from typing import Optional

from .entry_base import EntryPointBase
from ..errors import AOCClientError


class DownloadInputEntryPoint(EntryPointBase):

    @staticmethod
    def argdef(sp: _SubParsersAction) -> ArgumentParser:
        ap: ArgumentParser = sp.add_parser(
            "download-input",
            help="Download the given day's input and save it to a file."
        )
        ap.add_argument(
            "--day",
            default=datetime.now().day,
            required=False,
            help="The day of the input to download. Default: today",
            type=int,
        )
        ap.add_argument(
            "PATH",
            default="input.txt",
            help="The path to save the input data.",
            nargs='?'
        )
        return ap

    def run(self) -> Optional[int]:
        try:
            input = self.aoc_client.get_input(self.opts.day, self.config.get_year())
            with open(self.opts.PATH, "w") as fd:
                fd.write(input)
        except AOCClientError as err:
            self.log.exception("Failed to download input file")
