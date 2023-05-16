from domain.event import Event

class FlakeRequested(Event):
    """
    Represents the event when a Nix flake for a Python package has been requested
    """

    def __init__(
        self,
        packageName: str,
        packageVersion: str,
    ):
        """Creates a new FlakeRequested instance"""
        self._package_name = packageName
        self._package_version = packageVersion

    @property
    def package_name(self):
        return self._package_name

    @property
    def package_version(self):
        return self._package_version

    def __str__(self):
        return f'{{ "name": "{__name__}", "package_name": "{self._package_name}", "package_version": "{self._package_version}" }}'
