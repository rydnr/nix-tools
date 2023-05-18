import toml
from typing import Dict


class PyprojecttomlUtils:
    """
    Utilities for dealing with pyproject.toml files
    """

    @classmethod
    def parse_toml(cls, contents: str) -> Dict:
        return toml.loads(contents)

    @classmethod
    def read_pyproject_toml(cls, gitRepo) -> Dict:
        result = {}
        if gitRepo:
            pyprojecttoml_contents = gitRepo.get_file("pyproject.toml")

            if pyprojecttoml_contents:
                result = cls.parse_toml(pyprojecttoml_contents)
        return result
