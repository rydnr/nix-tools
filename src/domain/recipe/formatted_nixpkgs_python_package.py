from domain.python_package import PythonPackage
from domain.recipe.formatted_python_package import FormattedPythonPackage


class FormattedNixpkgsPythonPackage(FormattedPythonPackage):
    """
    Augments PythonPackage class for nixpkgs packages to include formatting logic required by recipe templates.
    """

    def __init__(self, pkg: PythonPackage):
        """Creates a new instance"""
        super().__init__(pkg)

    def as_parameter_to_package_nix(self) -> str:
        return self._pkg.name

    def overrides(self) -> str:
        return "TODO: {self._pkg.name}"
