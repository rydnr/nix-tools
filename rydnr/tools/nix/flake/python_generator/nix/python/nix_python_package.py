# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/nix/python/nix_python_package.py

This file defines the NixPythonPackage class.

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
import re


class NixPythonPackage(Entity):
    """
    Represents a Python package in Nix.
    """

    def __init__(self, name: str, version: str):
        """Creates a new NixPythonPackage instance"""
        super().__init__()
        self._name = name
        self._version = version

    @property
    @primary_key_attribute
    def name(self) -> str:
        return self._name

    @property
    @primary_key_attribute
    def version(self) -> str:
        return self._version

    def nixpkgs_package_name(self) -> str:
        """
        Retrieves the package name in nixpkgs
        """
        result = self.name
        match = re.search(r"[^.]+$|$", self.name)
        if match:
            result = match.group()
        return result

    def is_compatible_with(self, versionSpec: str) -> bool:
        """
        Checks if this package is compatible with given version spec.
        """
        result = True
        # TODO: support specs, not just values.
        # Split version strings into lists of integers
        version1_parts = [int(part) for part in self.version.split(".")]
        version2_parts = [int(part) for part in versionSpec.split(".")]

        # Compare each part of the versions
        for v1, v2 in zip(version1_parts, version2_parts):
            if v1 < v2:
                result = False
                break

        return result


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
