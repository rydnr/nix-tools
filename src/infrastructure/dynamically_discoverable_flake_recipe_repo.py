from domain.flake import Flake
from domain.flake_recipe import FlakeRecipe
from domain.flake_recipe_repo import FlakeRecipeRepo
from domain.recipe.base_flake_recipe import BaseFlakeRecipe

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
        for module_info in pkgutil.walk_packages(package.__path__, prefix=package.__name__ + "."):
            if module_info.name in sys.path:
                module = sys.modules[module_info.name]
            else:
                module = importlib.import_module(module_info.name)
            for name, obj in module.__dict__.items():
                if all(obj != recipeClass and isinstance(obj, type) and issubclass(obj, recipeClass) for recipeClass in [ FlakeRecipe, BaseFlakeRecipe ]):
                    recipe_classes.append(obj)
                    obj.initialize()
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
        cls._recipe_classes = cls.discover_recipes(module)

    def find_recipe_classes_by_flake(self, flake: Flake) -> List[FlakeRecipe]:
        """
        Retrieves the recipe classes matching given flake, if any.
        """
        similarities = {}
        for recipeClass in self.__class__._recipe_classes:
            similarities[recipeClass] = recipeClass.similarity(flake)
        result = sorted([aux for aux in similarities.keys() if similarities[aux] != 0.0], key=lambda recipeClass: similarities[recipeClass], reverse=True)

        if len(result) > 0:
            logging.getLogger(__name__).debug(f'Recipes for {flake.name}-{flake.version}: {result}')

        return result
