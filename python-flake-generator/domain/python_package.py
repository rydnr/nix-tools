from entity import Entity, attribute
from ports import Ports
from git_repo import GitRepo
from git_repo_repo import GitRepoRepo

from typing import Dict
import toml

class PythonPackage(Entity):
    """
    Represents a Python package.
    """
    def __init__(self, name: str, version: str, info: Dict, release: Dict):
        """Creates a new PythonPackage instance"""
        super().__init__(id)
        self._name = name
        self._version = version
        self._info = info
        self._release = release
        self._gitRepo = self.analyze_repo()

    @property
    @attribute
    def name(self) -> str:
        return self._name

    @property
    @attribute
    def version(self) -> str:
        return self._version

    @property
    @attribute
    def info(self) -> Dict:
        return self._info

    @property
    @attribute
    def release(self) -> Dict:
        return self._release

    @property
    @attribute
    def git_repo(self) -> Dict:
        return self._gitRepo

    def analyze_repo(self) -> GitRepo:
        return Ports.instance().resolve(GitRepoRepo).find_by_url_and_rev(self._info["home_page"], self._info["version"])

    def _parse_toml(self, contents: str):
        return toml.loads(contents)

    def get_package_type(self) -> str:
        result = "setuptools"
        pyprojecttoml_contents = self._gitRepo.pyproject_toml()

        if pyprojecttoml_contents:
            pyprojecttoml = self._parse_toml(pyprojecttoml_contents)

            build_system_requires = pyprojecttoml.get("build-system", {}).get("requires", [])
            if any(item.startswith("poetry") for item in build_system_requires):
                result = "poetry"
            elif any(item.startswith("flit") for item in build_system_requires):
                result = "flit"
            elif self._gitRepo.pipfile():
                result = "pipenv"

        return result
