# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/flake/flake_repo.py

This file defines the FlakeRepo class.

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
from domain.flake.flake import Flake
from domain.flake.flake_created import FlakeCreated
from domain.flake.recipe.flake_recipe import FlakeRecipe
from domain.repo import Repo

from typing import Dict, List


class FlakeRepo(Repo):
    """
    A subclass of Repo that manages Flakes.
    """

    def __init__(self):
        """
        Creates a new FlakeRepo instance.
        """
        super().__init__(Flake)

    def find_by_name_and_version(self, name: str, version: str) -> Flake:
        """Retrieves a flake matching given name and version"""
        raise NotImplementedError(
            "find_by_name_and_version() must be implemented by subclasses"
        )

    def create(
        self, flake: Flake, content: List[Dict[str, str]], recipe: FlakeRecipe
    ) -> FlakeCreated:
        """Creates the flake"""
        raise NotImplementedError("create() must be implemented by subclasses")

    def url_for_flake(self, name: str, version: str) -> str:
        """Retrieves the url of given flake"""
        raise NotImplementedError("url_for_flake() must be implemented by subclasses")


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
