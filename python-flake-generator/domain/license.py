import sys
from pathlib import Path

base_folder = str(Path(__file__).resolve().parent.parent)
if base_folder not in sys.path:
    sys.path.append(base_folder)

from domain.entity import Entity, primary_key_attribute

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
        super().__init__(id)
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
