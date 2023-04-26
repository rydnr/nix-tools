import os
import inspect
from pathlib import Path
import sys
import toml

base_folder = str(Path(__file__).resolve().parent.parent)
if base_folder not in sys.path:
    sys.path.append(base_folder)

from domain.entity import Entity, primary_key_attribute
from domain.flake import Flake
from domain.recipe.empty_flake_section_in_recipe_toml import EmptyFlakeSectionInRecipeToml
from domain.recipe.missing_flake_section_in_recipe_toml import MissingFlakeSectionInRecipeToml
from domain.recipe.missing_flake_version_spec_in_recipe_toml import MissingFlakeVersionSpecInRecipeToml
from domain.recipe.missing_recipe_toml import MissingRecipeToml
from domain.recipe.more_than_one_flake_in_recipe_toml import MoreThanOneFlakeInRecipeToml

class FlakeRecipe(Entity):

    """
    Represents a nix flake recipe.
    """

    _flake_name = ""
    _flake_version_spec = ""

    def __init__(self, flake: Flake):
        """Creates a new flake recipe instance"""
        super().__init__(id)
        self._flake = flake

    @property
    @primary_key_attribute
    def flake(self) -> str:
        return self._flake

    @classmethod
    def initialize(cls):
        if cls.should_initialize():
            cls._flake_name, cls._flake_version_spec = cls.supported_flake_name_and_version_spec()

    @classmethod
    def should_initialize(cls) -> bool:
        return cls != FlakeRecipe

    @classmethod
    def supported_flake_name_and_version_spec(cls) -> tuple:
        recipe_folder = Path(inspect.getsourcefile(cls)).parent
        recipe_toml_file = os.path.join(recipe_folder, "recipe.toml")
        if not os.path.exists(recipe_toml_file):
            raise MissingRecipeToml(recipe_toml_file)
        recipe_toml_contents = ""
        with open(recipe_toml_file, "r") as file:
            recipe_toml_contents = file.read()
        recipe_toml = toml.loads(recipe_toml_contents)
        flake_specs = recipe_toml.get("flake", {})
        if not flake_specs:
            raise MissingFlakeSectionInRecipeToml(recipe_toml_file)
        entries = list(flake_specs.keys())
        if not entries or len(entries) == 0:
            raise EmptyFlakeSectionInRecipeToml(recipe_toml_file)
        if len(entries) > 1:
            raise MoreThanOneFlakeInRecipeToml(recipe_toml_file)
        flake = entries[0]
        version_spec = flake_specs.get(flake, "")
        if not version_spec:
            raise MissingFlakeVersionSpecInRecipeToml(recipe_toml_file)
        return (flake, version_spec)

    def process(self):
        "Performs the recipe tasks"
        raise NotImplementedError()

    @classmethod
    def compatible_version(version: str) -> bool:
        "Checks if given version is compatible"
        raise NotImplementedError()

    @classmethod
    def supports(cls, flake: flake) -> bool:
        "Checks if the recipe class supports given flake"
        raise NotImplementedError()

    @classmethod
    def similarity(cls, flake: Flake) -> float:
        result = 0.0
        if cls._flake_name == flake.name:
            if cls._flake_version_spec == flake.version:
                result = 1.0
            elif cls.compatible_version(flake.version):
                result = 0.9
            else:
                result = 0.7
        elif cls.supports(flake):
            result = 0.6
        return result
