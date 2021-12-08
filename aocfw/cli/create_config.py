from argparse import _SubParsersAction, ArgumentParser
from typing import Optional

from .entry_base import EntryPointBase


class CreateConfigEntryPoint(EntryPointBase):

    @staticmethod
    def argdef(sp: _SubParsersAction) -> ArgumentParser:
        ap: ArgumentParser = sp.add_parser(
            "create-config",
            help="Create a new configuration file."
        )
        ap.add_argument(
            "PATH",
            default=".aocfwrc",
            nargs='?',
            help="The path to the configuration file to create.",
            type=str,
        )
        return ap

    def run(self) -> Optional[int]:
        self.config.new(self.opts.PATH)
        val = input("What is your session cookie? ")
        self.config.set_session_token(val)
        val = input("What year are we talking about? ")
        self.config.set_year(val)
        self.log.info("New config file %s", self.opts.PATH)
