import sys
sys.path.insert(0, "domain")
from python_package_repo import PythonPackageRepo
from python_package import PythonPackage

from typing import Dict
import re
from packaging.specifiers import SpecifierSet
import logging
import requests

class PypiRepo(PythonPackageRepo):
    """
    A PythonPackageRepo that uses Pypi as store
    """

    def __init__(self):
        super().__init__()


    def find_by_name_and_version(self, package_name: str, package_version: str) -> Dict[str, str]:
        """
        Retrieves the PythonPackage matching given name and version.
        """
        logging.getLogger(__name__).debug(f"looking for {package_name} {package_version} in pypi.org")
        # If the package_version is an exact version, add '==' before it
        if re.match(r"^\d+(\.\d+)*(-?(rc|b)\d+)?$", package_version):
            package_version = f"=={package_version}"

        specifier_set = SpecifierSet(package_version)

        logging.getLogger(__name__).debug(f"Retrieving {package_name}{package_version} info from https://pypi.org/pypi/{package_name}/json")
        package_data = requests.get(f"https://pypi.org/pypi/{package_name}/json").json()
        package_info = package_data.get("info", {})
        versions = package_data["releases"].keys()

        compatible_versions = [v for v in versions if v in specifier_set]

        if not compatible_versions:
            raise Exception(f"No compatible versions found for {package_name} version {package_version}")

        latest_version = max(compatible_versions)
        latest_release = len(package_data.get("releases", [])[latest_version]) - 1
        release_info = package_data.get("releases", [[]])[latest_version][latest_release]

        return PythonPackage(package_name, latest_version, package_info, release_info)
