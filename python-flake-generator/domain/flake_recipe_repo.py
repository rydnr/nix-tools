import sys
from pathlib import Path

base_folder = str(Path(__file__).resolve().parent.parent)
if base_folder not in sys.path:
    sys.path.append(base_folder)

from domain.repo import Repo
from domain.flake_recipe import FlakeRecipe
from domain.flake import Flake

class FlakeRecipeRepo(Repo):
    """
    A subclass of Repo that manages Flake recipes.
    """

    def __init__(self):
        """
        Creates a new FlakeRecipeRepo instance.
        """
        super().__init__(FlakeRecipe)

    def find_by_flake(self, flake: Flake) -> FlakeRecipe:
        """Retrieves a recipe matching given flake"""
        raise NotImplementedError(
            "find_by_flake() must be implemented by subclasses"
        )
