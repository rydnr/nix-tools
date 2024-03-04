# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/flake/license.py

This file defines the License class.

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


PYPI_TO_NIX_LICENSE_MAPPING = {
    "Apache-2.0": "asl20",
    "Apache 2.0": "asl20",
    "MIT": "mit",
    "GPL-3.0": "gpl3",
    "GPL 3.0": "gpl3",
    "GPL-3.0+": "gpl3Plus",
    "GPL 3.0+": "gpl3Plus",
    "LGPL-3.0": "lgpl3",
    "LGPL 3.0": "lgpl3",
    "LGPL-3.0+": "lgpl3Plus",
    "LGPL 3.0+": "lgpl3Plus",
    "BSD-2-Clause": "bsd2",
    "BSD-2 Clause": "bsd2",
    "BSD-3-Clause": "bsd3",
    "BSD-3 Clause": "bsd3",
}


class License(Entity):

    """
    Represents a License.
    """

    def __init__(self, pypi: str, nix: str):
        """Creates a new License instance"""
        super().__init__()
        self._pypi = pypi
        self._nix = nix

    @property
    @primary_key_attribute
    def pypi(self) -> str:
        return self._pypi

    @property
    @primary_key_attribute
    def nix(self) -> str:
        return self._nix

    @classmethod
    def from_pypi(cls, pypi: str):
        nix = PYPI_TO_NIX_LICENSE_MAPPING.get(pypi, "")
        if nix == "":
            nix = "mit"

        return License(pypi, nix)


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
