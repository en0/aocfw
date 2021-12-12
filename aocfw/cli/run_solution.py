from argparse import ArgumentParser, _SubParsersAction
from typing import Optional

from .entry_base import EntryPointBase


class RunSolutionEntryPoint(EntryPointBase):

    @staticmethod
    def argdef(sp: _SubParsersAction) -> ArgumentParser:
        ap: ArgumentParser = sp.add_parser(
            "run-solution",
            help="Download the given day's input and save it to a file."
        )
        ap.add_argument(
            "--auto-submit",
            default=False,
            required=False,
            action="store_true",
            help="Submit the answer to AoC",
        )
        ap.add_argument(
            "--day",
            help="The day to run",
            required=True,
            type=int,
        )
        ap.add_argument(
            "--part",
            help="The part to run",
            required=True,
            type=int,
        )
        return ap

    def run(self) -> Optional[int]:
        from importlib import import_module
        from os import path, chdir, getcwd
        import sys
        dirn = f"{self.opts.day:02}"
        mod = f"p{self.opts.part}"

        pwd = getcwd()
        chdir(dirn)

        sys.path.insert(0, '')
        module = import_module(mod)
        solution = getattr(module, "Solution")
        ans = solution.check(source="input.txt")
        self.log.info("Answer: %s", ans)

        chdir(pwd)
        if self.opts.auto_submit:
            result = self.aoc_client.submit_answer(
                day=self.opts.day,
                year=self.config.get_year(),
                part=self.opts.part,
                value=ans)
            self.log.info(result)
