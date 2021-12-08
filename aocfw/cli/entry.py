from argparse import ArgumentParser, _SubParsersAction
from typing import Callable


class EntryPoint:

    _enteries = []

    @classmethod
    def register(
        cls,
        argdef: Callable[[_SubParsersAction], ArgumentParser],
        entry: Callable[[], int]
    ):
        cls._enteries.append((argdef, entry))

    @classmethod
    def get_opts(cls):
        ap = ArgumentParser()
        ap.add_argument('--config', default=".aocfwrc", type=str, help="Change configuration file")
        sp = ap.add_subparsers(help='sub-command help')

        for argdef, entry in cls._enteries:
            _ap = argdef(sp)
            _ap.set_defaults(_entry_point=entry)

        return ap.parse_args()

    @classmethod
    def main(cls):
        result = 0
        try:
            opts = cls.get_opts()
            result = opts._entry_point(opts)
        except Exception as ex:
            print(ex)
            result = 1
        finally:
            exit(result if result is not None else 0)


def main():
    EntryPoint.main()
