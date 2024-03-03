# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/python/pipenv_python_package.py

This file defines the PipenvPythonPackage class.

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
from domain.python.python_package import PythonPackage

from typing import Dict, List


class PipenvPythonPackage(PythonPackage):
    """
    Represents a pipenv-based Python package.
    """

    def __init__(
        self, name: str, version: str, info: Dict, release: Dict, gitRepo: GitRepo
    ):
        """Creates a new PipenvPythonPackage instance"""
        super().__init__(name, version, info, release, gitRepo)

    @classmethod
    def git_repo_matches(cls, gitRepo: GitRepo) -> bool:
        return gitRepo.get_file("Pipfile") is not None

    def get_type(self) -> str:
        """
        Retrieves the type.
        """
        return "pipenv"

    def get_native_build_inputs(self) -> List:
        raise NotImplementedError("pipenv is currently not supported")

    def get_propagated_build_inputs(self) -> List:
        raise NotImplementedError("pipenv is currently not supported")

    def get_build_inputs(self) -> List:
        raise NotImplementedError("pipenv is currently not supported")

    def get_optional_build_inputs(self) -> List:
        raise NotImplementedError("pipenv is currently not supported")

    def get_check_inputs(self) -> List:
        raise NotImplementedError("pipenv is currently not supported")


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
