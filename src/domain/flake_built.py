class FlakeBuilt:
    """
    Represents the event when a Nix flake for a Python package has been built successfully.
    """

    def __init__(self, packageName: str, packageVersion: str, flakeFolder: str):
        """Creates a new FlakeCreated instance"""
        self._package_name = packageName
        self._package_version = packageVersion
        self._flake_folder = flakeFolder

    @property
    def package_name(self):
        return self._package_name

    @property
    def package_version(self):
        return self._package_version

    @property
    def flake_folder(self):
        return self._flake_folder

    def __str__(self):
        return f'{{ "name": "{__name__}", "package_name": "{self._package_name}", "package_version": "{self._package_version}", "flake_folder": "{self._flake_folder}" }}'
