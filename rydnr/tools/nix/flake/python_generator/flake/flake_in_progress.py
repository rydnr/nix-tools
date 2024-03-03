# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/flake/flake_in_progress.py

This file defines the FlakeInProgress class.

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
from pythoneda.shared import attribute, EntityInProgress, primary_key_attribute
from rydnr.tools.nix.flake.python_generator.python import PythonPackage


class FlakeInProgress(EntityInProgress):
    """
    Represents a flake which doesn't have all information yet.
    """

    def __init__(self, name: str, version: str, flakesFolder: str):
        """Creates a new FlakeInProgress instance"""
        super().__init__()
        self._name = name
        self._version = version
        self._flakes_folder = flakesFolder
        self._python_package = None

    @property
    @primary_key_attribute
    def name(self) -> str:
        return self._name

    @property
    @primary_key_attribute
    def version(self) -> str:
        return self._version

    @property
    @attribute
    def flakes_folder(self) -> str:
        return self._flakes_folder

    @property
    @attribute
    def python_package(self) -> PythonPackage:
        return self._python_package

    def set_python_package(pythonPackage: PythonPackage):
        self._python_package = pythonPackage


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
