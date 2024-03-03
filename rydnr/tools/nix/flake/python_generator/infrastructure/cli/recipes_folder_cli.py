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
from domain.primary_port import PrimaryPort

import argparse
import os
from pathlib import Path


class RecipesFolderCli(PrimaryPort):

    """
    A PrimaryPort that configures the recipes folder from the command line.
    """

    def __init__(self):
        super().__init__()

    def priority(self) -> int:
        return 2

    async def accept(self, app):
        parser = argparse.ArgumentParser(
            description="Parses the folder with the custom flakes"
        )
        parser.add_argument(
            "-r", "--recipes_folder", required=False, help="The flakes folder"
        )
        args, unknown_args = parser.parse_known_args()
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
