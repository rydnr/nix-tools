# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/nix/nix_template.py

This file defines the NixTemplate class.

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
from pythoneda.shared import attribute, Entity, primary_key_attribute
from rydnr.tools.nix.flake.python_generator.flake.recipe.recipe_does_not_support_placeholder import (
    RecipeDoesNotSupportPlaceholder,
)
from datetime import datetime
import logging
import string


class NixTemplate(Entity):

    """
    Represents a nix template.
    """

    def __init__(self, folder: str, path: str, contents: str):
        """Creates a new nix template instance"""
        super().__init__()
        self._folder = folder
        self._path = path
        self._contents = contents

    @property
    @primary_key_attribute
    def folder(self) -> str:
        return self._folder

    @property
    @primary_key_attribute
    def path(self) -> str:
        return self._path

    @property
    @attribute
    def contents(self) -> str:
        return self._contents

    def render(self, flake, recipe) -> str:
        logging.getLogger(__name__).debug(f"Generating the content of {self.path}")

        newline = "\n"
        tab = "\t"
        path = self.path
        folder = self.folder
        timestamp = datetime.now()

        return eval(f"""f'''{self._contents}'''""")


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
