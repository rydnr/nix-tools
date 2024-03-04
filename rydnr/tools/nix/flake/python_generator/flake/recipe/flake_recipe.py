# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/flake/recipe/flake_recipe.py

This file defines the FlakeRecipe class.

Copyright (C) 2023-today rydnr's rydnr/python-nix-flake-generator

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from pythoneda.shared import Entity, primary_key_attribute

# from rydnr.tools.nix.flake.python_generator.flake import Flake
from rydnr.tools.nix.flake.python_generator.flake.recipe import (
    EmptyFlakeMetadataSectionInRecipeToml,
    EmptyFlakeSectionInRecipeToml,
    MissingFlakeSectionInRecipeToml,
    MissingFlakeVersionSpecInRecipeToml,
    MissingRecipeToml,
    MissingTypeInFlakeMetadataSectionInRecipeToml,
    MoreThanOneFlakeInRecipeToml,
)

import inspect
import logging
import os
from pathlib import Path
import toml
from typing import Dict, List


class FlakeRecipe(Entity):

    """
    Represents a nix flake recipe.
    """

    _flakes = []

    def __init__(self, flake):
        """Creates a new flake recipe instance"""
        super().__init__()
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
                raise MissingTypeInFlakeMetadataSectionInRecipeToml(
                    cls.recipe_toml_file()
                )
        return result

    def process(self):  # -> FlakeCreated:
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
    def similarity(cls, flake) -> float:  #: Flake) -> float:
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
        logging.getLogger(cls.__name__).debug(
            f"Similarity between recipe {cls.__name__} and flake {flake.name}-{flake.version}: {result}"
        )
        return result

    def usesGitrepoSha256(self):
        return False

    def usesPipSha256(self):
        return False

    def remove_duplicates(self, *lists) -> List:
        result = []
        for lst in lists:
            for item in lst:
                if item not in result:
                    result.append(item)
        return result


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
