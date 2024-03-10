# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/infrastructure/cli/recipes_folder_cli.py

This file defines the RecipesFolderCli class.

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
import os
from pathlib import Path
from pythoneda.shared import PrimaryPort
from pythoneda.shared.application import PythonEDA
from pythoneda.shared.infrastructure.cli import CliHandler


class RecipesFolderCli(CliHandler, PrimaryPort):

    """
    A PrimaryPort that configures the recipes folder from the command line.

    Class name: RecipesFolderCli

    Responsibilities:
        - Parse the command-line to retrieve the information about the recipes folder.

    Collaborators:
        - PythonEDA subclasses: They are notified back with the information retrieved from the command line.
    """

    def __init__(self):
        """
        Creates a new RecipesFolderCli instance.
        """
        super().__init__("Provide the folder with the recipes")

    @classmethod
    def priority(cls) -> int:
        """
        Retrieves the priority of this port.
        :return: The priority.
        :rtype: int
        """
        return 2

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
            "-r", "--recipes_folder", required=False, help="The flakes folder"
        )

    async def handle(self, app: PythonEDA, args):
        """
        Processes the command specified from the command line.
        :param app: The PythonEDA instance.
        :type app: pythoneda.shared.application.PythonEDA
        :param args: The CLI args.
        :type args: argparse.args
        """
        recipes_folder = args.recipes_folder
        if not recipes_folder:
            recipes_folder = os.path.join(
                str(Path(__file__).resolve().parent.parent.parent.parent), "recipes"
            )
        await app.accept_recipes_folder(recipes_folder)


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
