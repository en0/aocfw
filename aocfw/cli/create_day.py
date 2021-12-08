import requests
from os import mkdir, path
from argparse import _SubParsersAction, ArgumentParser
from configparser import ConfigParser
from datetime import datetime

from .entry import EntryPoint


def get_opts(sp: _SubParsersAction):
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


def main(opts):
    cp = ConfigParser()
    cp.read(opts.config)
    year = cp.get("calendar", "year")
    dir_name = opts.PATH or f"{opts.day:02}"

    mkdir(dir_name)

    with open(path.join(dir_name, "p1.py"), "w") as fd:
        fd.writelines([
            "from typing import Iterable\n",
            "from aocfw import SolutionBase\n",
            "\n",
            "\n",
            "class Solution(SolutionBase):\n",
            "    def solve(self, data: Iterable[int]) -> int:\n",
            "        raise NotImplementedError()\n",
            "\n",
            "\n",
            "if __name__ == '__main__':\n",
            "    Solution.run(source='input.txt')\n",
            "\n",
        ])

    with open(path.join(dir_name, "p2.py"), "w") as fd:
        fd.writelines([
            "from typing import Iterable\n",
            "from aocfw import SolutionBase\n",
            "\n",
            "\n",
            "class Solution(SolutionBase):\n",
            "    def solve(self, data: Iterable[int]) -> int:\n",
            "        raise NotImplementedError()\n",
            "\n",
            "\n",
            "if __name__ == '__main__':\n",
            "    Solution.run(source='input.txt')\n",
            "\n",
        ])

    with open(path.join(dir_name, "p1_test.py"), "w") as fd:
        fd.writelines([
            "from unittest import TestCase, main\n",
            "from aocfw import TestCaseMixin\n",
            "from p1 import Solution\n",
            "\n",
            "\n",
            "class SolutionTests(TestCase, TestCaseMixin):\n",
            "\n",
            "    solution = Solution\n",
            "    source = 'sample.txt'\n",
            "    given = None\n",
            "\n",
            "\n",
            "if __name__ == '__main__':\n",
            "    main()\n",
            "\n",
        ])

    with open(path.join(dir_name, "p2_test.py"), "w") as fd:
        fd.writelines([
            "from unittest import TestCase, main\n",
            "from aocfw import TestCaseMixin\n",
            "from p2 import Solution\n",
            "\n",
            "\n",
            "class SolutionTests(TestCase, TestCaseMixin):\n",
            "\n",
            "    solution = Solution\n",
            "    source = 'sample.txt'\n",
            "    given = None\n",
            "\n",
            "\n",
            "if __name__ == '__main__':\n",
            "    main()\n",
            "\n",
        ])

    with open(path.join(dir_name, "sample.txt"), "w") as fd:
        fd.write("PUT SAMPLE HERE")

    url = f"https://adventofcode.com/{year}/day/{opts.day}/input"
    result = requests.get(url, cookies={"session": cp.get("creds", "token")})
    if result.status_code == 200:
        with open(path.join(dir_name, "input.txt"), "w") as fd:
            fd.write(result.text)
    else:
        print("Not able to download input data.")

    print("Don't forget to put something in sample.txt")


EntryPoint.register(get_opts, main)
