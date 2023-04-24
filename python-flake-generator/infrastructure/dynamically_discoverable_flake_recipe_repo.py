import sys
import os
import pkgutil
import importlib
from pathlib import Path

base_folder = str(Path(__file__).resolve().parent.parent)
if base_folder not in sys.path:
    sys.path.append(base_folder)
import domain.recipes

from domain.flake_recipe_repo import FlakeRecipeRepo
from domain.flake_recipe import FlakeRecipe
from domain.base_flake_recipe import BaseFlakeRecipe
from domain.specific_flake_recipe import SpecificFlakeRecipe
from domain.flake import Flake

# Discover and import modules under the 'domain.recipes' package and its subpackages
def discover_modules(package):
    for module_info in pkgutil.walk_packages(package.__path__, prefix=package.__name__ + "."):
        module = importlib.import_module(module_info.name)

discover_modules(domain.recipes)

def discover_recipes(package):
    recipe_classes = []
    for module_info in pkgutil.walk_packages(package.__path__, prefix=package.__name__ + "."):
        module = importlib.import_module(module_info.name)
        for name, obj in module.__dict__.items():
            if all(obj != recipeClass and isinstance(obj, type) and issubclass(obj, recipeClass) for recipeClass in [ FlakeRecipe, BaseFlakeRecipe ]):
                recipe_classes.append(obj)
    return recipe_classes

RECIPE_CLASSES = discover_recipes(domain.recipes)

class DynamicallyDiscoverableFlakeRecipeRepo(FlakeRecipeRepo):

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

        for recipe_class in RECIPE_CLASSES:
            if recipe_class.matches(flake):
                if issubclass(recipe_class, SpecificFlakeRecipe):
                    specific_matches.append(recipe_class)
                else:
                    generic_matches.append(recipe_class)

        if specific_matches:
            result = specific_matches[0]
        elif generic_matches:
            result = generic_matches[0]
        else:
            result = None

        return result
