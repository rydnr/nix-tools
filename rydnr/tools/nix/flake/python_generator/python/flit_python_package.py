# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/python/flit_python_package.py

This file defines the FlitPythonPackage class.

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
from pythoneda.shared import Ports
from rydnr.tools.nix.flake.python_generator.git import GitRepo
from rydnr.tools.nix.flake.python_generator.python import PythonPackage

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

    def get_type(self) -> str:
        """
        Retrieves the type.
        """
        return "flit"

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


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
