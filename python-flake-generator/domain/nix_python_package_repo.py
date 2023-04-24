import sys
from pathlib import Path

base_folder = str(Path(__file__).resolve().parent.parent)
if base_folder not in sys.path:
    sys.path.append(base_folder)

from domain.repo import Repo
from domain.nix_python_package import NixPythonPackage

from typing import List

class NixPythonPackageRepo(Repo):
    """
    A subclass of Repo that manages Nix Python Packages.
    """

    def __init__(self):
        """
        Creates a new NixPythonPackageRepo instance.
        """
        super().__init__(NixPythonPackage)

    def find_by_name(self, package_name: str) -> List[NixPythonPackage]:
        """
        Retrieves the NixPythonPackages matching given name and version.
        """
        raise NotImplementedError("find_by_name() must be implemented by subclasses")

    def find_by_name_and_version(self, package_name: str, package_version: str) -> NixPythonPackage:
        """
        Retrieves the NixPythonPackages matching given name and version.
        """
        raise NotImplementedError("find_by_name_and_version() must be implemented by subclasses")
