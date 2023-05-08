from domain.python_package import PythonPackage

class FormattedPythonPackage():
    """
    Augments PythonPackage class to include formatting logic required by recipe templates.
    """
    def __init__(self, pkg: PythonPackage):
        """Creates a new instance"""
        self._pkg = pkg

    @property
    def pkg(self) -> PythonPackage:
        return self._pkg

    def as_parameter_to_package_nix() -> str:
        raise NotImplementedError("as_parameter_to_package_nix() must be implemented by subclasses")

    def __str__(self):
        return self._pkg.__str__()

    def __getattr__(self, attr):
        """
        Delegate any method call to the wrapped instance.
        """
        return getattr(self._pkg, attr)

    def __eq__(self, other):
        return self._pkg.__eq__(other)

    def __hash__(self):
        return self._pkg.__hash__()
