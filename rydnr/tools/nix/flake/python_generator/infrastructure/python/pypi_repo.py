from domain.python.python_package_factory import PythonPackageFactory
from domain.python.python_package_metadata import PythonPackageMetadata
from domain.python.python_package_metadata_repo import PythonPackageMetadataRepo

import logging
from packaging.specifiers import SpecifierSet
import re
import requests
from typing import Dict, List

class PypiRepo(PythonPackageMetadataRepo):
    """
    A PythonPackageMetadataRepo that uses Pypi as store
    """

    _cached_packages = {}
    _cached_package_data = {}

    def __init__(self):
        super().__init__()

    def retrieve_package_data(self, package_name: str) -> Dict:
        result = self.__class__._cached_package_data.get(package_name, None)
        if result is None:
            logging.getLogger(__name__).debug(f"Retrieving {package_name} info from https://pypi.org/pypi/{package_name}/json")
            result = requests.get(f"https://pypi.org/pypi/{package_name}/json").json()
            self.__class__._cached_package_data[package_name] = result
        return result

    async def find_by_name_and_version(self, package_name: str, package_version: str) -> PythonPackageMetadata:
        """
        Retrieves the metadata of the PythonPackage matching given name and version.
        """
        result = self.__class__._cached_packages.get(f'{package_name}-{package_version}', None)
        if result is None:
            logger = logging.getLogger(__name__)
            package_data = self.retrieve_package_data(package_name)

            # If the package_version is an exact version, add '==' before it
            if re.match(r"^\d+(\.\d+)*(-?(rc|b)\d+)?$", package_version):
                package_version = f"=={package_version}"

            specifier_set = SpecifierSet(package_version)

            package_info = package_data.get("info", {})
            versions = package_data["releases"].keys()

            compatible_versions = [v for v in versions if v in specifier_set]

            if compatible_versions:
                latest_version = max(compatible_versions)
                latest_release = len(package_data.get("releases", [])[latest_version]) - 1
                release_info = package_data.get("releases", [[]])[latest_version][latest_release]

                result = await PythonPackageMetadata(package_name, latest_version, package_info, release_info)
                self.__class__._cached_packages[f'{package_name}-{latest_version}'] = result
                self.__class__._cached_packages[f'{package_name}-{package_version}'] = result

        return result

    async def find_all_by_name(self, package_name: str) -> List[PythonPackageMetadata]:
        """Retrieves the metadata of all versions of the PythonPackage matching given name."""
        result = []
        logger = logging.getLogger(__name__)
        logger.debug(f"Looking for all versions of {package_name} in pypi.org")

        package_data = self.retrieve_package_data(package_name)

        package_info = package_data.get("info", {})
        versions = package_data["releases"].keys()

        for version in versions:
            latest_release = len(package_data.get("releases", [])[version]) - 1
            release_info = package_data.get("releases", [[]])[version][latest_release]
            package = self.__class__._cached_packages.get(f'{package_name}-{latest_version}', None)
            if package is None:
                await PythonPackageMetadata(package_name, latest_version, package_info, release_info)
                self.__class__._cached_packages[f'{package_name}-{latest_version}'] = package

            result.append(package)

        return result

    async def find_by_name(self, package_name: str) -> PythonPackageMetadata:
        """Retrieves the metadata of the latest version of the PythonPackage matching given name."""
        logger = logging.getLogger(__name__)
        package_data = self.retrieve_package_data(package_name)

        package_info = package_data.get("info", {})
        versions = package_data["releases"].keys()

        latest_version = max(versions)
        latest_release = len(package_data.get("releases", [])[latest_version]) - 1
        release_info = package_data.get("releases", [[]])[latest_version][latest_release]

        result = self.__class__._cached_packages.get(f'{package_name}-{latest_version}', None)
        if result is None:
            result = PythonPackageMetadata(package_name, latest_version, package_info, release_info)
            self.__class__._cached_packages[f'{package_name}-{latest_version}'] = result

        return result
