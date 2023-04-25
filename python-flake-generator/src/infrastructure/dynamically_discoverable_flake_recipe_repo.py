import importlib
import os
from pathlib import Path
import pkgutil
import sys

base_folder = str(Path(__file__).resolve().parent.parent)
if base_folder not in sys.path:
    sys.path.append(base_folder)

import domain
from domain.flake_recipe_repo import FlakeRecipeRepo
from domain.flake_recipe import FlakeRecipe
from domain.base_flake_recipe import BaseFlakeRecipe
from domain.specific_flake_recipe import SpecificFlakeRecipe
from domain.flake import Flake


class DynamicallyDiscoverableFlakeRecipeRepo(FlakeRecipeRepo):

    _recipes_folder = None
    _recipe_classes = {}

    @classmethod
    def recipes_folder(cls, folder: str):
        cls._recipes_folder = folder

    @classmethod
    def discover_modules(cls, package):
        """Discover and import modules under the 'recipes' package and its subpackages."""
        for module_info in pkgutil.walk_packages(package.__path__, prefix=package.__name__ + "."):
            if module_info.name in sys.path:
                module = sys.modules[module_info.name]
            else:
                module = importlib.import_module(module_info.name)


    @classmethod
    def discover_recipes(cls, package):
        recipe_classes = []
        for module_info in pkgutil.walk_packages(package.__path__, prefix=package.__name__ + "."):
            if module_info.name in sys.path:
                module = sys.modules[module_info.name]
            else:
                module = importlib.import_module(module_info.name)
            for name, obj in module.__dict__.items():
                if all(obj != recipeClass and isinstance(obj, type) and issubclass(obj, recipeClass) for recipeClass in [ FlakeRecipe, BaseFlakeRecipe ]):
                    recipe_classes.append(obj)
        return recipe_classes

    @classmethod
    def initialize(cls):
        for f in [ str(Path(cls._recipes_folder).resolve().parent), cls._recipes_folder ]:
            if f not in sys.path:
                sys.path.append(f)
        moduleName = Path(cls._recipes_folder).stem
        if moduleName in sys.modules:
            module = sys.modules[moduleName]
        else:
            module = importlib.import_module(moduleName)
        cls.discover_modules(module)
        cls._recipe_classes = cls.discover_recipes(module)

    """
    A FlakeRecipeRepo that discovers recipes dynamically.
    """
    def find_by_flake(self, flake: Flake) -> FlakeRecipe:
        """
        Retrieves the recipe matching given flake, if any.
        """
        result = None
        specific_matches = []
        generic_matches = []

        for recipe_class in self.__class__._recipe_classes:
            if recipe_class.matches(flake):
                if issubclass(recipe_class, SpecificFlakeRecipe):
                    specific_matches.append(recipe_class)
                else:
                    generic_matches.append(recipe_class)

        if specific_matches:
            result = specific_matches[0](flake)
        elif generic_matches:
            result = generic_matches[0](flake)
        else:
            result = None

        return result
