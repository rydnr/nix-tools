# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/nix/python/nix_python_package_in_nixpkgs.py

This file defines the NixPythonPackageInNixpkgs class.

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
from domain.event import Event
from domain.python.python_package import PythonPackage
from domain.value_object import primary_key_attribute


class NixPythonPackageInNixpkgs(Event):
    """
    Represents the event when a Nix flake for a Python package is already available
    """

    def __init__(self, pkg: PythonPackage):
        """Creates a new NixPythonPackageInNixpkgs instance"""
        self._python_package = pkg

    @property
    @primary_key_attribute
    def python_package(self):
        return self._python_package


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
