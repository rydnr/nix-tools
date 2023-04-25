import sys
from pathlib import Path

base_folder = str(Path(__file__).resolve().parent.parent.parent.parent)
if base_folder not in sys.path:
    sys.path.append(base_folder)

from domain.base_flake_recipe import BaseFlakeRecipe
from domain.specific_flake_recipe import SpecificFlakeRecipe
from domain.flake import Flake
from domain.ports import Ports

class PytestAsyncio_0_19_0(BaseFlakeRecipe, SpecificFlakeRecipe):

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
