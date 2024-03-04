# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/infrastructure/flake/recipe/dynamically_discoverable_flake_recipe_repo.py

This file defines the DynamicallyDiscoverableFlakeRecipeRepo class.

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
from rydnr.tools.nix.flake.python_generator.flake.flake import Flake
from rydnr.tools.nix.flake.python_generator.flake.recipe.flake_recipe import FlakeRecipe
from rydnr.tools.nix.flake.python_generator.flake.recipe.flake_recipe_repo import (
    FlakeRecipeRepo,
)
from rydnr.tools.nix.flake.python_generator.flake.recipe.base_flake_recipe import (
    BaseFlakeRecipe,
)

import importlib
from pathlib import Path
import pkgutil
import logging
import sys
from typing import List


class DynamicallyDiscoverableFlakeRecipeRepo(FlakeRecipeRepo):

    """
    Repository than dynamically discovers flake recipes under a given folder.
    """

    _recipes_folder = None
    _recipe_classes = {}

    @classmethod
    def recipes_folder(cls, folder: str):
        cls._recipes_folder = folder

    @classmethod
    def discover_recipes(cls, package):
        recipe_classes = []
        for module_info in pkgutil.walk_packages(
            package.__path__, prefix=package.__name__ + "."
        ):
            if module_info.name in sys.path:
                module = sys.modules[module_info.name]
            else:
                module = importlib.import_module(module_info.name)
            for name, obj in module.__dict__.items():
                if all(
                    obj != recipeClass
                    and isinstance(obj, type)
                    and issubclass(obj, recipeClass)
                    for recipeClass in [FlakeRecipe, BaseFlakeRecipe]
                ):
                    recipe_classes.append(obj)
                    obj.initialize()
        return recipe_classes

    @classmethod
    def initialize(cls):
        for f in [str(Path(cls._recipes_folder).resolve().parent), cls._recipes_folder]:
            if f not in sys.path:
                sys.path.append(f)
        moduleName = Path(cls._recipes_folder).stem
        if moduleName in sys.modules:
            module = sys.modules[moduleName]
        else:
            module = importlib.import_module(moduleName)
        cls._recipe_classes = cls.discover_recipes(module)

    def find_recipe_classes_by_flake(self, flake: Flake) -> List[FlakeRecipe]:
        """
        Retrieves the recipe classes matching given flake, if any.
        """
        similarities = {}
        for recipeClass in self.__class__._recipe_classes:
            similarities[recipeClass] = recipeClass.similarity(flake)
        result = sorted(
            [aux for aux in similarities.keys() if similarities[aux] != 0.0],
            key=lambda recipeClass: similarities[recipeClass],
            reverse=True,
        )

        if len(result) > 0:
            logging.getLogger(__name__).debug(
                f"Recipes for {flake.name}-{flake.version}: {result}"
            )

        return result


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
