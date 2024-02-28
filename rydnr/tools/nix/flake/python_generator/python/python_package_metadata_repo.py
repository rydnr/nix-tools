from domain.python.python_package_metadata import PythonPackageMetadata
from domain.repo import Repo

from typing import List

class PythonPackageMetadataRepo(Repo):
    """
    A subclass of Repo that manages metadata of Python Packages.
    """

    def __init__(self):
        """
        Creates a new PythonPackageMetadataRepo instance.
        """
        super().__init__(PythonPackageMetadata)

    async def find_by_name_and_version(self, package_name: str, version_spec: str) -> PythonPackageMetadata:
        """Retrieves the metadata of the PythonPackage matching given name and version."""
        raise NotImplementedError(
            "find_by_name_and_version() must be implemented by subclasses"
        )

    async def find_by_name(self, package_name: str) -> PythonPackageMetadata:
        """Retrieves the metadata of the latest version of the PythonPackage matching given name."""
        raise NotImplementedError(
            "find_by_name() must be implemented by subclasses"
        )

    async def find_all_by_name(self, package_name: str) -> List[PythonPackageMetadata]:
        """Retrieves the metadata for all versions of the PythonPackage matching given name."""
        raise NotImplementedError(
            "find_all_by_name() must be implemented by subclasses"
        )
