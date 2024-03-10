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
from argparse import ArgumentParser
from pythoneda.shared import PrimaryPort
from pythoneda.shared.application import PythonEDA
from pythoneda.shared.infrastructure.cli import CliHandler
from rydnr.tools.nix.flake.python_generator.flake.build.build_flake_requested import (
    BuildFlakeRequested,
)


class BuildFlakeCli(CliHandler, PrimaryPort):

    """
    A PrimaryPort used to build flakes.

    Class name: BuildFlakeCli

    Responsibilities:
        - Parse the command-line to retrieve the information about the repository folder.

    Collaborators:
        - PythonEDA subclasses: They are notified back with the information retrieved from the command line.
    """

    def __init__(self):
        """
        Creates a new BuildFlakeCli instance.
        """
        super().__init__("Builds a flake")

    """
    A PrimaryPort that sends BuildFlake commands specified from the command line.
    """

    @classmethod
    def priority(cls) -> int:
        """
        Retrieves the priority of this port.
        :return: The priority.
        :rtype: int
        """
        return 90

    @classmethod
    @property
    def is_one_shot_compatible(cls) -> bool:
        """
        Retrieves whether this primary port should be instantiated when
        "one-shot" behavior is active.
        It should return False unless the port listens to future messages
        from outside.
        :return: True in such case.
        :rtype: bool
        """
        return True

    def add_arguments(self, parser: ArgumentParser):
        """
        Defines the specific CLI arguments.
        :param parser: The parser.
        :type parser: argparse.ArgumentParser
        """
        parser.add_argument(
            "-b",
            "--build",
            action="store_true",
            help="Whether to build a Nix flake",
        )

    async def handle(self, app: PythonEDA, args):
        """
        Processes the command specified from the command line.
        :param app: The PythonEDA instance.
        :type app: pythoneda.shared.application.PythonEDA
        :param args: The CLI args.
        :type args: argparse.args
        """
        if args.build:
            if app.package_name and app.package_version and app.flakes_folder:
                event = BuildFlakeRequested(
                    app.package_name,
                    app.package_version,
                    app.flakes_folder,
                    None,  # pythonPackage
                )
                await app.accept(event)
            else:
                self.__class__.logger().error(
                    f"-pn|--package-name ({app.package_name}), -pv|--package-version ({app.package_version}) and -f|--flakes-folder ({app.flakes_folder}) are required"
                )


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
