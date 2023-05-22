from domain.entity_in_progress import EntityInProgress
from domain.python.python_package_metadata import PythonPackageMetadata
from domain.value_object import attribute, primary_key_attribute


class PythonPackageInProgress(EntityInProgress):

    """
    Represents a PythonPackage which doesn't have all information yet.
    """
    def __init__(self, name: str, version: str, metadata: PythonPackageMetadata):
        """Creates a new PythonPackageInProgress instance"""
        super().__init__()
        self._name = name
        self._version = version
        self._metadata = metadata

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
    def metadata(self) -> PythonPackageMetadata:
        return self._metadata
