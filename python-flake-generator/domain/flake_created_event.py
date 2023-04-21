class FlakeCreated():
    """
    Represents the event when a Nix flake for a Python package has been created
    """
    def __init__(self, packageName: str, packageVersion: str):
        """Creates a new CreateFlakeCommand instance"""
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
