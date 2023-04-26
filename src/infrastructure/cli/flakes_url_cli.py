from domain.primary_port import PrimaryPort

import argparse

class FlakesUrlCli(PrimaryPort):

    """
    A PrimaryPort that configures the flakes url from the command line.
    """

    def __init__(self):
        super().__init__()

    def priority(self) -> int:
        return 2

    def accept(self, app):

        parser = argparse.ArgumentParser(
            description="Parses the Flakes url"
        )
        parser.add_argument(
            "-u", "--flakes_url", required=True, help="The flakes url"
        )
        args, unknown_args = parser.parse_known_args()
        app.accept_flakes_url(args.flakes_url)
