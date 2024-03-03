# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/flake/recipe/formatted_flake_python_package.py

This file defines the FormattedFlakePythonPackage class.

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
from domain.python.python_package import PythonPackage
from domain.flake.recipe.formatted_python_package import FormattedPythonPackage


class FormattedFlakePythonPackage(FormattedPythonPackage):
    """
    Augments PythonPackage class for flake-based packages to include formatting logic required by recipe templates.
    """

    def __init__(self, pkg: PythonPackage):
        """Creates a new instance"""
        super().__init__(pkg)

    def flake_declaration(self) -> str:
        return f'{self._formatted.name}-flake.url = "{self._formatted.flake_url()}";'

    def as_parameter_to_package_nix(self) -> str:
        return f"{self._formatted.name} = {self._formatted.name}-flake.packages.${{system}}.{self._formatted.name};"


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
