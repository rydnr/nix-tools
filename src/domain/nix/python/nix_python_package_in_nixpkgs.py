from domain.event import Event

class NixPythonPackageInNixpkgs(Event):
    """
    Represents the event when a Nix flake for a Python package is already available
    """

    def __init__(
        self,
        pythonPackage: pkg
    ):
        """Creates a new NixPythonPackageInNixpkgs instance"""
        self._python_package = pkg

    @property
    def python_package(self):
        return self._python_package

    def __str__(self):
        return f'{{ "name": "{__name__}", "python_package": "{self._python_package}" }}'

    def __repr__(self):
        return f'{{ "name": "{__name__}", "python_package": "{self._python_package.__repr__()}" }}'
