# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/flake/recipe/__init__.py

This file ensures rydnr.tools.nix.flake.python_generator.flake.recipe is a namespace.

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
__path__ = __import__("pkgutil").extend_path(__path__, __name__)

from .base_flake_recipe import BaseFlakeRecipe
from .empty_flake_metadata_section_in_recipe_toml import (
    EmptyFlakeMetadataSectionInRecipeToml,
)
from .empty_flake_section_in_recipe_toml import EmptyFlakeSectionInRecipeToml
from .flake_recipe import FlakeRecipe
from .flake_recipe_repo import FlakeRecipeRepo
from .formatted_flake import FormattedFlake
from .formatted_flake_python_package import FormattedFlakePythonPackage
from .formatted_nixpkgs_python_package import FormattedNixpkgsPythonPackage
from .formatted_python_package import FormattedPythonPackage
from .formatted_python_package_list import FormattedPythonPackageList
from .missing_flake_section_in_recipe_toml import MissingFlakeSectionInRecipeToml
from .missing_flake_version_spec_in_recipe_toml import (
    MissingFlakeVersionSpecInRecipeToml,
)
from .missing_recipe_toml import MissingRecipeToml
from .missing_type_in_flake_metadata_section_in_recipe_toml import (
    MissingTypeInFlakeMetadataSectionInRecipeToml,
)
from .more_than_one_flake_in_recipe_toml import MoreThanOneFlakeInRecipeToml
from .recipe_does_not_support_placeholder import RecipeDoesNotSupportPlaceholder

# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
