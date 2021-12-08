import requests
from argparse import _SubParsersAction, ArgumentParser
from configparser import ConfigParser
from datetime import datetime

from .entry import EntryPoint


def get_opts(sp: _SubParsersAction):
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


def main(opts):
    cp = ConfigParser()
    cp.read(opts.config)
    year = cp.get("calendar", "year")

    url = f"https://adventofcode.com/{year}/day/{opts.day}/input"
    result = requests.get(url, cookies={"session": cp.get("creds", "token")})
    if result.status_code == 200:
        with open(opts.PATH, "w") as fd:
            fd.write(result.text)
    else:
        print("Oops! Something is not right.")
        print(result.text)


EntryPoint.register(get_opts, main)
