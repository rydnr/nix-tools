from domain.entity import Entity, primary_key_attribute
from domain.flake import Flake
from domain.recipe.empty_flake_metadata_section_in_recipe_toml import EmptyFlakeMetadataSectionInRecipeToml
from domain.recipe.empty_flake_section_in_recipe_toml import EmptyFlakeSectionInRecipeToml
from domain.recipe.missing_flake_section_in_recipe_toml import MissingFlakeSectionInRecipeToml
from domain.recipe.missing_flake_version_spec_in_recipe_toml import MissingFlakeVersionSpecInRecipeToml
from domain.recipe.missing_recipe_toml import MissingRecipeToml
from domain.recipe.missing_type_in_flake_metadata_section_in_recipe_toml import MissingTypeInFlakeMetadataSectionInRecipeToml
from domain.recipe.more_than_one_flake_in_recipe_toml import MoreThanOneFlakeInRecipeToml

import os
import inspect
import logging
from pathlib import Path
import toml
from typing import Dict,List

class FlakeRecipe(Entity):

    """
    Represents a nix flake recipe.
    """

    _flakes = []

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
            cls._flakes = cls.supported_flakes()
            cls._type = cls.flake_type()

    @classmethod
    def should_initialize(cls) -> bool:
        return cls != FlakeRecipe

    @classmethod
    def recipe_toml_file(cls) -> str:
        recipe_folder = Path(inspect.getsourcefile(cls)).parent
        return os.path.join(recipe_folder, "recipe.toml")

    @classmethod
    def read_recipe_toml(cls):
        result = ""
        recipe_toml_file = cls.recipe_toml_file()
        if not os.path.exists(recipe_toml_file):
            raise MissingRecipeToml(recipe_toml_file)
        recipe_toml_contents = ""
        with open(recipe_toml_file, "r") as file:
            recipe_toml_contents = file.read()
        result = toml.loads(recipe_toml_contents)
        return result

    @classmethod
    def supported_flakes(cls) -> List[Dict[str, str]]:
        result = []
        recipe_toml = cls.read_recipe_toml()
        flake_specs = recipe_toml.get("flake", {})
        if not flake_specs:
            raise MissingFlakeSectionInRecipeToml(cls.recipe_toml_file())
        entries = list(flake_specs.keys())
        if not entries or len(entries) == 0:
            raise EmptyFlakeSectionInRecipeToml(cls.recipe_toml_file())
        for flake in entries:
            version_spec = flake_specs.get(flake, "")
            if not version_spec:
                raise MissingFlakeVersionSpecInRecipeToml(flake, cls.recipe_toml_file())
            aux = {}
            aux[flake] = version_spec
            result.append(aux)
        return result

    @classmethod
    def flake_type(cls) -> str:
        result = None
        recipe_toml = cls.read_recipe_toml()
        flake_metadata = recipe_toml.get("flake").get("metadata", {})
        if flake_metadata:
            result = flake_metadata.get("type", None)
            if not result:
                raise MissingTypeInFlakeMetadataSectionInRecipeToml(cls.recipe_toml_file())
        return result

    def process(self): # -> FlakeCreated:
        "Performs the recipe tasks"
        raise NotImplementedError()

    @classmethod
    def compatible_versions(cls, v1: str, v2: str) -> bool:
        "Checks if given versions are compatible"
        raise NotImplementedError()

    @classmethod
    def supports(cls, flake: flake) -> bool:
        "Checks if the recipe class supports given flake"
        raise NotImplementedError()

    @classmethod
    def type_matches(cls, flake) -> bool:
        return cls._type == flake.python_package.get_type()

    @classmethod
    def similarity(cls, flake: Flake) -> float:
        result = 0.0
        partialResults = []
        if cls.supports(flake):
            return 1.0
        if cls.type_matches(flake):
            partialResults.append(0.5)
        for entry in cls._flakes:
            partialResult = 0.0
            name = list(entry.keys())[0]
            version = entry[name]
            if name == flake.name:
                if version == flake.version:
                    return 1.0
                elif cls.compatible_versions(version, flake.version):
                    partialResult = 0.9
                else:
                    partialResult = 0.7
            partialResults.append(partialResult)
        result = max(partialResults)
        logging.getLogger(cls.__name__).debug(f'Similarity between recipe {cls.__name__} and flake {flake.name}-{flake.version}: {result}')
        return result

    def usesGitrepoSha256(self):
        return False

    def usesPipSha256(self):
        return False
