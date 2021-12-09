from argparse import ArgumentParser, _SubParsersAction
from typing import Optional

from .entry_base import EntryPointBase


class RunSolutionEntryPoint(EntryPointBase):

    @staticmethod
    def argdef(sp: _SubParsersAction) -> ArgumentParser:
        ap: ArgumentParser = sp.add_parser(
            "experimental-run-solution",
            help="Download the given day's input and save it to a file."
        )
        ap.add_argument(
            "path",
            help="The path to the file containing the solution.",
            type=str,
        )
        return ap

    def run(self) -> Optional[int]:
        from importlib import import_module
        from os import path, chdir
        import sys
        dirn = path.dirname(self.opts.path)
        base = path.basename(self.opts.path)
        chdir(dirn)
        sys.path.insert(0, '')
        module = import_module(base[:-3])
        solution = getattr(module, "Solution")
        ans = solution.check(source="input.txt")
        self.log.info("Answer: %s", ans)
        #self.aoc_client.submit_answer(self.opts.day, self.config.get_year(), self.opts.part, ans)
