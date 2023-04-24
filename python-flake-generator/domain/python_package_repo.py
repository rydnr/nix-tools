import sys
from pathlib import Path

base_folder = str(Path(__file__).resolve().parent.parent)
if base_folder not in sys.path:
    sys.path.append(base_folder)

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
        """Must be implemented by subclasses"""
        raise NotImplementedError(
            "find_by_name_and_version() must be implemented by subclasses"
        )
