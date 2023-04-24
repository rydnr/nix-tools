import sys
from pathlib import Path

base_folder = str(Path(__file__).resolve().parent.parent)
if base_folder not in sys.path:
    sys.path.append(base_folder)

from domain.entity import Entity, primary_key_attribute

import re

class NixPythonPackage(Entity):
    """
    Represents a Python package in Nix.
    """

    def __init__(self, name: str, version: str):
        """Creates a new NixPythonPackage instance"""
        super().__init__(id)
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
        result = self.name
        match = re.search(r'[^.]+$|$', self.name)
        if match:
            result = match.group()
        return result
