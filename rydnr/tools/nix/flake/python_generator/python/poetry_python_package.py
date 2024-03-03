# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/python/poetry_python_package.py

This file defines the PoetryPythonPackage class.

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
from domain.ports import Ports
from domain.git.git_repo import GitRepo
from domain.python.build.pyprojecttoml_utils import PyprojecttomlUtils
from domain.python.python_package import PythonPackage

from typing import Dict, List


class PoetryPythonPackage(PythonPackage, PyprojecttomlUtils):
    """
    Represents a Poetry-based Python package.
    """

    def __init__(
        self, name: str, version: str, info: Dict, release: Dict, gitRepo: GitRepo
    ):
        """Creates a new PoetryPythonPackage instance"""
        super().__init__(name, version, info, release, gitRepo)

    @classmethod
    def read_poetry_lock(cls, gitRepo) -> Dict:
        result = {}
        if gitRepo:
            poetrylock_contents = gitRepo.get_file("poetry.lock")

            if poetrylock_contents:
                result = cls.parse_toml(poetrylock_contents)
        return result

    @classmethod
    def git_repo_matches(cls, gitRepo: GitRepo) -> bool:
        result = False
        pyproject_toml = cls.read_pyproject_toml(gitRepo)

        if pyproject_toml:
            build_system_requires = pyproject_toml.get("build-system", {}).get(
                "requires", []
            )
            if any(item.startswith("poetry") for item in build_system_requires):
                result = True
        return result

    def get_type(self) -> str:
        """
        Retrieves the type.
        """
        return "poetry"

    def get_poetry_deps(self, section: str) -> List:
        result = []
        pyproject_toml = self.__class__.read_pyproject_toml(self.git_repo)
        if pyproject_toml:
            poetry_lock = self.__class__.read_poetry_lock(self.git_repo)
            if poetry_lock:
                for dev_dependency in list(
                    pyproject_toml.get("tool", {})
                    .get("poetry", {})
                    .get(section, {})
                    .keys()
                ):
                    for package in poetry_lock["package"]:
                        if package.get("name", "") == dev_dependency:
                            pythonPackage = (
                                Ports.instance()
                                .resolvePythonPackageRepo()
                                .find_by_name_and_version(
                                    dev_dependency, package.get("version", "")
                                )
                            )
                            if pythonPackage:
                                result.append(pythonPackage)

        return result

    def get_native_build_inputs(self) -> List:
        return self.get_poetry_deps("dev-dependencies")

    def get_propagated_build_inputs(self) -> List:
        return self.get_poetry_deps("dependencies")

    def get_build_inputs(self) -> List:
        return self.get_poetry_deps("dependencies")

    def get_optional_build_inputs(self) -> List:
        return self.get_poetry_deps("extras")

    def get_check_inputs(self) -> List:
        return self.get_poetry_deps("test")


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
