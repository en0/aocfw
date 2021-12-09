from argparse import _SubParsersAction, ArgumentParser
from datetime import datetime
from typing import Optional

from .entry_base import EntryPointBase
from ..errors import AOCClientError


class SubmitAnswerEntryPoint(EntryPointBase):

    @staticmethod
    def argdef(sp: _SubParsersAction) -> ArgumentParser:
        ap: ArgumentParser = sp.add_parser(
            "submit-answer",
            help="Submit an answer."
        )
        ap.add_argument(
            "--day",
            default=datetime.now().day,
            required=False,
            help="The day of the input to download. Default: today",
            type=int,
        )
        ap.add_argument(
            "--part",
            required=True,
            choices=[1, 2],
            help="Part 1 or part 2",
            type=int,
        )
        ap.add_argument(
            "answer",
            help="The answer to submit."
        )
        return ap

    def run(self) -> Optional[int]:
        try:
            result = self.aoc_client.submit_answer(
                day=self.opts.day,
                year=self.config.get_year(),
                part=self.opts.part,
                value=self.opts.answer)
            self.log.info(result)
        except AOCClientError as ex:
            self.log.error(ex)
