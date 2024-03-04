# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/python/build/setuppy_strategy_found.py

This file defines the SetuppyStrategyFound event.

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
from pythoneda.shared import attribute
from rydnr.tools.nix.flake.python_generator.python.python_package_base_event import (
    PythonPackageBaseEvent,
)


class SetuppyStrategyFound(PythonPackageBaseEvent):
    """
    Represents the event triggered when a Python package can be built using setup.py.
    """

    def __init__(self, pythonPackage):  #: PythonPackage):
        """Creates a new PythonBuildStrategyRequested instance"""
        super().__init__(
            pythonPackage.name, pythonPackage.version, pythonPackage.git_repo
        )
        self._pythonPackage = pythonPackage

    @property
    @attribute
    def pythonPackage():  # -> PythonPackage:
        return self._pythonPackage


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
