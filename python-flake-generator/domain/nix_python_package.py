from entity import Entity, primary_key_attribute

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

