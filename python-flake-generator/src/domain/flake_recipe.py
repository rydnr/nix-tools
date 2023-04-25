import sys
from pathlib import Path

base_folder = str(Path(__file__).resolve().parent.parent)
if base_folder not in sys.path:
    sys.path.append(base_folder)

from domain.entity import Entity, primary_key_attribute
from domain.flake import Flake

class FlakeRecipe(Entity):

    """
    Represents a nix flake recipe.
    """
    def __init__(self, flake: Flake):
        """Creates a new flake recipe instance"""
        super().__init__(id)
        self._flake = flake

    @property
    @primary_key_attribute
    def flake(self) -> str:
        return self._flake

    @classmethod
    def matches(cls, flake) -> bool:
        "Checks whether this recipe matches given flake"
        raise NotImplementedError()

    def process(self):
        "Performs the recipe tasks"
        raise NotImplementedError()
