from domain.formatting import Formatting
from domain.python_package import PythonPackage

class FormattedPythonPackage(Formatting):
    """
    Augments PythonPackage class to include formatting logic required by recipe templates.
    """
    def __init__(self, pkg: PythonPackage):
        """Creates a new instance"""
        super().__init__(pkg)

    @property
    def pkg(self) -> PythonPackage:
        return self._fmt

    def as_parameter_to_package_nix() -> str:
        raise NotImplementedError("as_parameter_to_package_nix() must be implemented by subclasses")
