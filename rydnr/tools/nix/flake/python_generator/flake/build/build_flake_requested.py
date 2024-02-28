from domain.event import Event
from domain.python.python_package import PythonPackage
from domain.value_object import attribute, primary_key_attribute

class BuildFlakeRequested(Event):
    """
    Represents the event when building a Nix flake for a Python package has been requested
    """

    def __init__(
        self,
        packageName: str,
        packageVersion: str,
        flakesFolder: str,
        pythonPackage: PythonPackage
    ):
        """Creates a new BuildFlakeRequested instance"""
        self._package_name = packageName
        self._package_version = packageVersion
        self._flakes_folder = flakesFolder
        self._python_package = pythonPackage

    @property
    @primary_key_attribute
    def package_name(self):
        return self._package_name

    @property
    @primary_key_attribute
    def package_version(self):
        return self._package_version

    @property
    @attribute
    def flakes_folder(self):
        return self._flakes_folder

    @property
    @attribute
    def python_package(self):
        return self._python_package
