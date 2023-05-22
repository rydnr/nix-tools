from domain.event import Event
from domain.python.python_package import PythonPackage
from domain.value_object import primary_key_attribute

class NixPythonPackageInNixpkgs(Event):
    """
    Represents the event when a Nix flake for a Python package is already available
    """

    def __init__(
        self,
        pkg: PythonPackage
    ):
        """Creates a new NixPythonPackageInNixpkgs instance"""
        self._python_package = pkg

    @property
    @primary_key_attribute
    def python_package(self):
        return self._python_package
