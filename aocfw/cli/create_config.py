from argparse import _SubParsersAction, ArgumentParser
from configparser import ConfigParser

from .entry import EntryPoint


def get_opts(sp: _SubParsersAction):
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


def main(opts):
    cp = ConfigParser()
    cp.add_section("creds")
    cp.add_section("calendar")

    val = input("What is your session cookie? ")
    cp.set("creds", "token", val)

    val = input("What year are we talking about? ")
    cp.set("calendar", "year", val)

    with open(opts.PATH, "w") as fd:
        cp.write(fd)

    print(f"New config file: {opts.PATH}")

EntryPoint.register(get_opts, main)
