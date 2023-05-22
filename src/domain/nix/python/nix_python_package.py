from domain.entity import Entity
from domain.value_object import primary_key_attribute

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
        match = re.search(r'[^.]+$|$', self.name)
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
        version1_parts = [int(part) for part in self.version.split('.')]
        version2_parts = [int(part) for part in versionSpec.split('.')]

        # Compare each part of the versions
        for v1, v2 in zip(version1_parts, version2_parts):
            if v1 < v2:
                result = False
                break

        return result
