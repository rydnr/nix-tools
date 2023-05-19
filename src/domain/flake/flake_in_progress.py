from domain.entity import primary_key_attribute
from domain.entity_in_progress import EntityInProgress


class FlakeInProgress(EntityInProgress):
    """
    Represents a flake which doesn't have all information yet.
    """
    def __init__(self, name: str, version: str):
        """Creates a new FlakeInProgress instance"""
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
