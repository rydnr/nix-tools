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
        """
        Retrieves the package name in nixpkgs
        """
        result = self.name
        match = re.search(r'[^.]+$|$', self.name)
        if match:
            result = match.group()
        return result

    def is_compatible_with(self, versionSpec: str) -> bool:
        """
        Checks if this package is compatible with given version spec.
        """
        # TODO: implement pyproject.toml version rules
        return versionSpec == self.version
