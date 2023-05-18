from domain.python.python_package import PythonPackage
from domain.flake.recipe.formatted_python_package import FormattedPythonPackage


class FormattedFlakePythonPackage(FormattedPythonPackage):
    """
    Augments PythonPackage class for flake-based packages to include formatting logic required by recipe templates.
    """

    def __init__(self, pkg: PythonPackage):
        """Creates a new instance"""
        super().__init__(pkg)

    def flake_declaration(self) -> str:
        return f'{self._formatted.name}-flake.url = "{self._formatted.flake_url()}";'

    def as_parameter_to_package_nix(self) -> str:
        return f"{self._formatted.name} = {self._formatted.name}-flake.packages.${{system}}.{self._formatted.name};"
