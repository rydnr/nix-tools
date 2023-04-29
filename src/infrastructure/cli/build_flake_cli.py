from domain.build_flake_requested import BuildFlakeRequested
from domain.primary_port import PrimaryPort

import argparse
import logging


class BuildFlakeCli(PrimaryPort):

    """
    A PrimaryPort that sends BuildFlake commands specified from the command line.
    """

    def __init__(self):
        super().__init__()

    def priority(self) -> int:
        return 100

    def accept(self, app):

        parser = argparse.ArgumentParser(
            description="Builds a given flake"
        )
        parser.add_argument("packageName", help="The name of the Python package")
        parser.add_argument("packageVersion", help="The version of the Python package")
        parser.add_argument(
            "-f", "--flakes_folder", required=False, help="The folder containing the flakes"
        )
        # TODO: Check how to avoid including flags from other cli handlers such as the following
        parser.add_argument(
            "-t", "--github_token", required=False, help="The github token"
        )
        parser.add_argument("-u", "--flakes_url", required=False, help="The flakes url")
        args, unknown_args = parser.parse_known_args()

        event = BuildFlakeRequested(args.packageName, args.packageVersion, args.flakes_folder)

        logging.getLogger(__name__).debug(f"Requesting the building of flake {event.package_name}-{event.package_version} to {app}")
        app.accept_event(event)
