from domain.entity_in_progress import EntityInProgress
from domain.python.python_package import PythonPackage
from domain.value_object import attribute, primary_key_attribute


class FlakeInProgress(EntityInProgress):
    """
    Represents a flake which doesn't have all information yet.
    """
    def __init__(self, name: str, version: str, flakesFolder: str):
        """Creates a new FlakeInProgress instance"""
        super().__init__()
        self._name = name
        self._version = version
        self._flakes_folder = flakesFolder
        self._python_package = None

    @property
    @primary_key_attribute
    def name(self) -> str:
        return self._name

    @property
    @primary_key_attribute
    def version(self) -> str:
        return self._version

    @property
    @attribute
    def flakes_folder(self) -> str:
        return self._flakes_folder

    @property
    @attribute
    def python_package(self) -> PythonPackage:
        return self._python_package

    def set_python_package(pythonPackage: PythonPackage):
        self._python_package = pythonPackage
