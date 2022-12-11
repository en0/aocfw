import sys, stat
from argparse import ArgumentParser, _SubParsersAction
from glob import glob
from importlib import import_module, reload
from os import path, chdir, getcwd, lstat, system
from time import sleep
from typing import Optional, Dict
from multiprocessing import Process

from .entry_base import EntryPointBase


class TestSolutionEntryPoint(EntryPointBase):

    @staticmethod
    def argdef(sp: _SubParsersAction) -> ArgumentParser:
        ap: ArgumentParser = sp.add_parser(
            "test-solution",
            help="Test the given day's solution."
        )
        ap.add_argument(
            "--auto-submit",
            default=False,
            required=False,
            action="store_true",
            help="After unittests pass, submit the answer to AoC",
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
        ap.add_argument(
            "--test-command",
            help="The unit test command to run. Example: pytest --log-cli-level=DEBUG {mod}.py",
            default="env python -m unittest {mod}",
        )
        ap.add_argument(
            "--watch",
            help="Wait for changes and rerun tests.",
            action="store_true",
            default=False,
        )
        return ap

    def run(self) -> Optional[int]:

        dirn = f"{self.opts.day:02}"
        mod = f"p{self.opts.part}_test"
        cmd = self.opts.test_command.format(mod=mod)

        pwd = getcwd()
        chdir(dirn)
        sys.path.insert(0, '')

        def run_tests():
            if system(cmd) == 0 and self.opts.auto_submit:
                r = input("The tests pass. Do you want to go for it? (y/n) ")
                if r != 'y':
                    self.log.info("Disabling auto-submit")
                    self.opts.auto_submit = False
                else:
                    # Run the actual input
                    module = import_module(mod)
                    solution = getattr(module, "Solution")
                    ans = solution.check(source="input.txt")
                    self.log.info("Answer: %s", ans)

                    # Submit to aoc
                    chdir(pwd)
                    result = self.aoc_client.submit_answer(
                        day=self.opts.day,
                        year=self.config.get_year(),
                        part=self.opts.part,
                        value=ans)
                    self.log.info(result)
                    return 'exit_now'

        if run_tests() == 'exit_now':
            return

        if not self.opts.watch:
            return

        files = {f: 0 for f in glob("*.py") + glob("*.txt")}
        self.update_mtime(files)

        while True:
            if self.update_mtime(files) > 0:
                if run_tests() == 'exit_now':
                    return
            else:
                sleep(1)

    def update_mtime(self, files: Dict[str, float]) -> int:
        changes = 0
        for file in files.keys():
            mtime = lstat(file).st_mtime
            if mtime != files[file]:
                changes += 1
            files[file] = mtime
        return changes
