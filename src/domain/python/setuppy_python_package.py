from domain.ports import Ports
from domain.git_repo import GitRepo
from domain.python_package import PythonPackage

from typing import Dict, List


class SetuppyPythonPackage(PythonPackage):
    """
    Represents a setup.py-based Python package.
    """

    def __init__(
        self, name: str, version: str, info: Dict, release: Dict, gitRepo: GitRepo
    ):
        """Creates a new SetuppyPythonPackage instance"""
        super().__init__(name, version, info, release, gitRepo)

    @classmethod
    def git_repo_matches(cls, gitRepo: GitRepo) -> bool:
        return gitRepo.get_file("setup.py") is not None

    def get_native_build_inputs(self) -> List:
        raise NotImplementedError("setup.py is currently not supported")

    def get_propagated_build_inputs(self) -> List:
        raise NotImplementedError("setup.py is currently not supported")

    def get_build_inputs(self) -> List:
        raise NotImplementedError("setup.py is currently not supported")

    def get_optional_build_inputs(self) -> List:
        raise NotImplementedError("setup.py is currently not supported")

    def get_check_inputs(self) -> List:
        raise NotImplementedError("setup.py is currently not supported")
