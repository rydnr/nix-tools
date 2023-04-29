class BuildFlakeRequested:
    """
    Represents the event when building a Nix flake for a Python package has been requested
    """

    def __init__(
        self,
        packageName: str,
        packageVersion: str,
        flakesFolder: str
    ):
        """Creates a new BuildFlakeRequested instance"""
        self._package_name = packageName
        self._package_version = packageVersion
        self._flakes_folder = flakesFolder

    @property
    def package_name(self):
        return self._package_name

    @property
    def package_version(self):
        return self._package_version

    @property
    def flakes_folder(self):
        return self._flakes_folder

    def __str__(self):
        return f'{{ "name": "{__name__}", "package_name": "{self._package_name}", "package_version": "{self._package_version}", "flakes_folder": "{self._flakes_folder}" }}'
