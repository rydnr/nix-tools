# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/infrastructure/cli/build_flake_cli.py

This file defines the BuildFlakeCli class.

Copyright (C) 2023-today rydnr's rydnr/python-nix-flake-generator

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from domain.flake.build.build_flake_requested import BuildFlakeRequested
from domain.primary_port import PrimaryPort

import argparse
import logging


class BuildFlakeCli(PrimaryPort):

    """
    A PrimaryPort that sends BuildFlake commands specified from the command line.
    """

    def priority(self) -> int:
        return 100

    async def accept(self, app):
        parser = argparse.ArgumentParser(description="Builds a given flake")
        parser.add_argument(
            "command",
            choices=["create", "build"],
            nargs="?",
            default=None,
            help="Whether to generate a nix flake",
        )
        parser.add_argument("packageName", help="The name of the Python package")
        parser.add_argument("packageVersion", help="The version of the Python package")
        parser.add_argument(
            "-f",
            "--flakes_folder",
            required=False,
            help="The folder containing the flakes",
        )
        # TODO: Check how to avoid including flags from other cli handlers such as the following
        parser.add_argument(
            "-t", "--github_token", required=False, help="The github token"
        )
        parser.add_argument("-u", "--flakes_url", required=False, help="The flakes url")
        parser.add_argument(
            "-x",
            "--forensic_folder",
            required=False,
            help="The folder where to copy the contents of flakes whose build failed",
        )
        args, unknown_args = parser.parse_known_args()

        if args.command == "build":
            event = BuildFlakeRequested(
                args.packageName, args.packageVersion, args.flakes_folder
            )
            logging.getLogger(__name__).debug(
                f"Requesting the building of flake {event.package_name}-{event.package_version} to {app}"
            )
            await app.accept(event)


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
