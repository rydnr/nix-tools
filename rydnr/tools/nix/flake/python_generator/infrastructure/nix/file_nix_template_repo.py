# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/infrastructure/nix/file_nix_template_repo.py

This file defines the FileNixTemplateRepo class.

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
from rydnr.tools.nix.flake.python_generator.flake.recipe.flake_recipe import FlakeRecipe
from rydnr.tools.nix.flake.python_generator.nix.nix_template_repo import NixTemplateRepo
from rydnr.tools.nix.flake.python_generator.nix.nix_template import NixTemplate

import os
from pathlib import Path
import sys
from typing import Dict, List


class FileNixTemplateRepo(NixTemplateRepo):
    """
    A NixTemplateRepo using files.
    """

    _recipes_folder = None

    @classmethod
    def recipes_folder(cls, folder: str):
        cls._recipes_folder = folder

    def __init__(self):
        super().__init__()

    def find_flake_templates_by_recipe(
        self, recipe: FlakeRecipe
    ) -> List[Dict[str, NixTemplate]]:
        """Retrieves the flake templates for given recipe"""
        result = []

        for tmpl_file in (
            Path(sys.modules[recipe.__class__.__module__].__file__)
            .parent.resolve()
            .glob("**/*.tmpl")
        ):
            if tmpl_file.is_file():
                template_name = tmpl_file.stem
                file_base = template_name
                folder = f"{recipe.flake.name}-{recipe.flake.version}"
                if template_name == "package.nix":
                    file_base = f"{folder}.nix"
                relative_path = os.path.join(folder, file_base)
                template = {}
                template["base_folder"] = self.__class__._recipes_folder
                template["folder"] = folder
                template["template"] = str(tmpl_file)
                template["basename"] = file_base
                template["path"] = relative_path
                template["contents"] = self.read_file(tmpl_file)
                result.append(template)
        return result

    def read_file(self, filePath: str) -> str:
        result = ""
        with open(filePath, "r") as file:
            result = file.read()
        return result


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
