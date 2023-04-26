from domain.flake import Flake
from domain.recipe.base_flake_recipe import BaseFlakeRecipe

class PytestAsyncio_0_19_0(BaseFlakeRecipe):

    """
    Represents a nix flake recipe for pytest-asyncio-0.19.0
    """
    def __init__(self, flake: Flake):
        """Creates a new pytest-asyncio-0.19.0 flake recipe instance"""
        super().__init__(id)
        self._flake = flake

    @classmethod
    def matches(cls, flake):
        return flake.name == "pytest-asyncio" and flake.version == "0.19.0"
