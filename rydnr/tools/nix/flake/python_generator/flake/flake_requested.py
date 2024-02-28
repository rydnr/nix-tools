from domain.event import Event
from domain.value_object import attribute, primary_key_attribute


class FlakeRequested(Event):
    """
    Represents the event when a Nix flake for a Python package has been requested
    """

    def __init__(
        self,
        packageName: str,
        packageVersion: str,
        flakesFolder: str
    ):
        """Creates a new FlakeRequested instance"""
        super().__init__()
        self._package_name = packageName
        self._package_version = packageVersion
        self._flakes_folder = flakesFolder

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
