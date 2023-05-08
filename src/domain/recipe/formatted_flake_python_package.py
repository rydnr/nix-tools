from domain.python_package import PythonPackage
from domain.recipe.formatted_python_package import FormattedPythonPackage


class FormattedFlakePythonPackage(FormattedPythonPackage):
    """
    Augments PythonPackage class for flake-based packages to include formatting logic required by recipe templates.
    """

    def __init__(self, pkg: PythonPackage):
        """Creates a new instance"""
        super().__init__(pkg)

    def flake_declaration() -> str:
        return f'{self._pkg.name}-flake.url = "{self._pkg.flake_url()}";'

    def as_parameter_to_package_nix() -> str:
        return f"{self._pkg.name} = {self._pkg.name}-flake.packages.${{system}}.{self._pkg.name};"
