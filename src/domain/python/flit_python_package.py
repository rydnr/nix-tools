from domain.ports import Ports
from domain.git_repo import GitRepo
from domain.python_package import PythonPackage

import toml
from typing import Dict, List


class FlitPythonPackage(PythonPackage):
    """
    Represents a Flit-based Python package.
    """

    def __init__(
        self, name: str, version: str, info: Dict, release: Dict, gitRepo: GitRepo
    ):
        """Creates a new FlitPythonPackage instance"""
        super().__init__(name, version, info, release, gitRepo)

    @classmethod
    def parse_toml(cls, contents: str) -> Dict:
        return toml.loads(contents)

    @classmethod
    def read_pyproject_toml(cls, gitRepo: GitRepo) -> Dict:
        result = {}
        if gitRepo:
            pyprojecttoml_contents = gitRepo.get_file("pyproject.toml")

            if pyprojecttoml_contents:
                result = cls.parse_toml(pyprojecttoml_contents)
        return result

    @classmethod
    def git_repo_matches(cls, gitRepo: GitRepo) -> bool:
        result = False
        pyproject_toml = cls.read_pyproject_toml(gitRepo)

        if pyproject_toml:
            build_system_requires = pyproject_toml.get("build-system", {}).get(
                "requires", []
            )
            if any(item.startswith("flit") for item in build_system_requires):
                result = True
        return result

    def get_native_build_inputs(self) -> List:
        raise NotImplementedError("flit is currently not supported")

    def get_propagated_build_inputs(self) -> List:
        raise NotImplementedError("flit is currently not supported")

    def get_build_inputs(self) -> List:
        raise NotImplementedError("flit is currently not supported")

    def get_optional_build_inputs(self) -> List:
        raise NotImplementedError("flit is currently not supported")

    def get_check_inputs(self) -> List:
        raise NotImplementedError("flit is currently not supported")
