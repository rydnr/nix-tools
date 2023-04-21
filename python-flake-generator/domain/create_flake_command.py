class CreateFlake():
    """
    Represents the command to create a Nix flake for a Python package
    """
    def __init__(self, packageName: str, packageVersion: str):
        """Creates a new CreateFlake instance"""
        self._packageName = packageName
        self._packageVersion = packageVersion

    @property
    def packageName(self):
        return self._packageName

    @property
    def packageVersion(self):
        return self._packageVersion


    def __str__(self):
        return f'{{ "packageName": "{self._packageName}", "packageVersion": "{self._packageVersion}" }}'
