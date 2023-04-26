import sys
from pathlib import Path

base_folder = str(Path(__file__).resolve().parent.parent)
if base_folder not in sys.path:
    sys.path.append(base_folder)

from domain.primary_port import PrimaryPort
from domain.create_flake_command import CreateFlake

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


    def old_args(app):
        parser = argparse.ArgumentParser(description="Generates flakes from templates for packages in poetry.lock not available in nixpkgs")
        parser.add_argument("poetryLockFile", help="The poetry.lock file")
        parser.add_argument("baseFolder", help="The base folder for the flakes")
        parser.add_argument("githubToken", help="The github token")
        return parser.parse_args()

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
