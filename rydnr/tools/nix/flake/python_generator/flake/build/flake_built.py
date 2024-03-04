# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/flake/build/flake_built.py

This file defines the FlakeBuilt class.

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
from pythoneda.shared import Event


class FlakeBuilt(Event):
    """
    Represents the event when a Nix flake for a Python package has been built successfully.
    """

    def __init__(self, packageName: str, packageVersion: str, flakeFolder: str):
        """Creates a new FlakeCreated instance"""
        self._package_name = packageName
        self._package_version = packageVersion
        self._flake_folder = flakeFolder

    @property
    def package_name(self):
        return self._package_name

    @property
    def package_version(self):
        return self._package_version

    @property
    def flake_folder(self):
        return self._flake_folder

    def __str__(self):
        return f'{{ "name": "{__name__}", "package_name": "{self._package_name}", "package_version": "{self._package_version}", "flake_folder": "{self._flake_folder}" }}'


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
