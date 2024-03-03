# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/python/python_package_created.py

This file defines the PythonPackageCreated event.

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
from rydnr.tools.nix.flake.python_generator.python import PythonPackage


class PythonPackageCreated(Event):
    """
    Represents the event when a PythonPackage has been created.
    """

    def __init__(self, package: PythonPackage):
        """Creates a new PythonPackageCreated instance"""
        self._package = package

    @property
    def package(self):
        return self._package

    def __str__(self):
        return f'{{ "name": "{__name__}", "package": "{self._package}" }}'


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
