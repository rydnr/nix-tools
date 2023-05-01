from domain.repo import Repo
from domain.python_package import PythonPackage

class PythonPackageRepo(Repo):
    """
    A subclass of Repo that manages Python Packages.
    """

    def __init__(self):
        """
        Creates a new PythonPackageRepo instance.
        """
        super().__init__(PythonPackage)

    def find_by_name_and_version(
        self, package_name: str, version_spec: str
    ) -> PythonPackage:
        """Retrieves the PythonPackage matching given name and version."""
        raise NotImplementedError(
            "find_by_name_and_version() must be implemented by subclasses"
        )

    def find_by_name(self, package_name: str) -> PythonPackage:
        """Retrieves latest version of the PythonPackage matching given name."""
        raise NotImplementedError(
            "find_by_name() must be implemented by subclasses"
        )
