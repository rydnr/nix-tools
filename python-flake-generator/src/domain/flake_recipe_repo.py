from pathlib import Path
import sys

base_folder = str(Path(__file__).resolve().parent.parent)
if base_folder not in sys.path:
    sys.path.append(base_folder)

from domain.flake import Flake
from domain.flake_recipe import FlakeRecipe
from domain.repo import Repo

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
