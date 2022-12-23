from os import mkdir, path
from argparse import _SubParsersAction, ArgumentParser, Namespace
from datetime import datetime
from typing import Optional, List

from .entry_base import EntryPointBase


class CreateDayEntryPoint(EntryPointBase):

    _dir_name: str

    @staticmethod
    def argdef(sp: _SubParsersAction) -> ArgumentParser:
        ap: ArgumentParser = sp.add_parser(
            "create-day",
            help="Create a new day from templates",
        )
        ap.add_argument(
            "--day",
            default=datetime.now().day,
            required=False,
            help="The day we are talking about. Default: today",
            type=int,
        )
        ap.add_argument(
            "PATH",
            default=None,
            help="Specify the directory name. Default: the number of today",
            nargs='?'
        )
        return ap

    def run(self) -> Optional[int]:
        self._mkdir(self.opts.PATH or f"{self.opts.day:02}")
        self._write_parser()
        self._write_puzzle(1)
        self._write_puzzle(2)
        self._write_out("sample.txt", "SAMPLE DATA HERE")
        self._write_input_file()
        self.log.info("Don't forget to put something in %s", path.join(self._dir_name, "sample.txt"))

    def _mkdir(self, dir_name: str) -> None:
        self._dir_name = dir_name
        mkdir(self._dir_name)

    def _write_parser(self) -> None:
        self._write_out("parser.py", lines=[
            r"from typing import IO, Iterable",
            r"from aocfw import IParser",
            r"",
            r"",
            r"class Parser(IParser):",
            r"    def parse(self, data: IO) -> Iterable[str]:",
            r"        return map(lambda x: str(x).rstrip('\n'), data)",
        ])

    def _write_input_file(self) -> None:
        try:
            input = self.aoc_client.get_input(self.opts.day, self.config.get_year())
            self._write_out("input.txt", input)
        except AOCClientError as err:
            self.log.exception("Failed to download input file")
            self._write_out("input.txt", "INPUT HERE")

    def _write_puzzle(self, part: int) -> None:
        self._write_out(f"p{part}.py", lines=[
            "from typing import Iterable",
            "from aocfw import SolutionBase, IParser",
            "from parser import Parser",
            "",
            "",
            "class Solution(SolutionBase):",
            "",
            "    bindings = {IParser: Parser}",
            "",
            "    def solve(self, data: Iterable[int]) -> int:",
            "        raise NotImplementedError()",
            "",
            "",
            "if __name__ == '__main__':",
            "    Solution.run(source='input.txt')",
            "",
        ])
        self._write_out(f"p{part}_test.py", lines=[
            "from unittest import TestCase, main",
            "from aocfw import TestCaseMixin",
            f"from p{part} import Solution",
            "",
            "",
            "class SolutionTests(TestCase, TestCaseMixin):",
            "",
            "    solution = Solution",
            "    source = 'sample.txt'",
            "    given = None",
            "",
            "",
            "if __name__ == '__main__':",
            "    main()",
            "",
        ])

    def _write_out(self, file_name: str, data: any = None, lines: List[str] = None) -> None:
        with open(path.join(self._dir_name, file_name), "w") as fd:
            if data is not None:
                fd.write(data)
            elif lines is not None:
                fd.write("\n".join(lines))

