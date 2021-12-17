from typing import Type, IO, List, Iterable
from contextlib import contextmanager

from .typing import ISolution


class TestCaseMixin:

    source: str = None
    mode: str = "r"
    sample: IO = None
    given: any = None
    solution: Type[ISolution] = None

    @contextmanager
    def context_sample(self, sample: List[str]) -> Iterable[any]:
        _source, self.source, _sample = self.source, None, self.sample
        try:
            self.sample = StringIO("\n".join(sample))
            yield self.get_parsed_data()
        finally:
            self.sample = _sample
            self.source = _source

    def get_source_args(self) -> dict:
        """Gets the correct source arguments based on test setup.

        You can override this method and handle arguments manually
        """
        if self.source is not None:
            return {"source": self.source, "mode": self.mode}
        elif self.sample is not None:
            return {"sample": self.sample}

    def get_parsed_data(self) -> any:
        args = self.get_source_args()
        return self.solution.parse(**args)

    def test_given(self) -> None:
        if self.given is None:
            print("No given value. Skipping test_given")
            return
        args = self.get_source_args()
        self.assertEqual(self.solution.check(**args), self.given)

