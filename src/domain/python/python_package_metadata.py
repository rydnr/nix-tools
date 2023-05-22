from domain.entity import Entity
from domain.value_object import attribute, primary_key_attribute

from typing import Dict

class PythonPackageMetadata(Entity):
    """
    Represents metadata of a Python package.
    """

    def __init__(self, name: str, version: str, info: Dict, release: Dict):
        """Creates a new PythonPackageMetadata instance"""
        super().__init__()
        self._name = name
        self._version = version
        self._info = info
        self._release = release

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
    def info(self) -> Dict:
        return self._info

    @property
    @attribute
    def release(self) -> Dict:
        return self._release

