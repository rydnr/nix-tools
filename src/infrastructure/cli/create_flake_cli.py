from domain.create_flake import CreateFlake
from domain.primary_port import PrimaryPort

import argparse
import logging

class CreateFlakeCli(PrimaryPort):

    """
    A PrimaryPort that sends CreateFlake commands specified from the command line.
    """
    def __init__(self):
        super().__init__()

    def priority(self) -> int:
        return 100

    def accept(self, app):

        parser = argparse.ArgumentParser(description="Generates a flake for a given Python package")
        parser.add_argument("packageName", help="The name of the Python package")
        parser.add_argument("packageVersion", help="The version of the Python package")
        # TODO: Check how to avoid including flags from other cli handlers such as the following
        parser.add_argument("-t", "--github_token", required=False, help="The github token")
        parser.add_argument("-f", "--flakes_folder", required=False, help="The flakes folder")
        parser.add_argument("-u", "--flakes_url", required=False, help="The flakes url")
        args, unknown_args = parser.parse_known_args()

        command = CreateFlake(args.packageName, args.packageVersion)

        logging.getLogger(__name__).debug(f'Sending command {command} to {app}')
        app.accept_create_flake(command)
