# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/infrastructure/python/pypi_repo.py

This file defines the PypiRepo class.

Copyright (C) 2023-today rydnr's rydnr/python-nix-flake-generator

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from rydnr.tools.nix.flake.python_generator.python.python_package_factory import (
    PythonPackageFactory,
)
from rydnr.tools.nix.flake.python_generator.python.python_package_metadata import (
    PythonPackageMetadata,
)
from rydnr.tools.nix.flake.python_generator.python.python_package_metadata_repo import (
    PythonPackageMetadataRepo,
)

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
            logging.getLogger(__name__).debug(
                f"Retrieving {package_name} info from https://pypi.org/pypi/{package_name}/json"
            )
            result = requests.get(f"https://pypi.org/pypi/{package_name}/json").json()
            self.__class__._cached_package_data[package_name] = result
        return result

    async def find_by_name_and_version(
        self, package_name: str, package_version: str
    ) -> PythonPackageMetadata:
        """
        Retrieves the metadata of the PythonPackage matching given name and version.
        """
        result = self.__class__._cached_packages.get(
            f"{package_name}-{package_version}", None
        )
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
                latest_release = (
                    len(package_data.get("releases", [])[latest_version]) - 1
                )
                release_info = package_data.get("releases", [[]])[latest_version][
                    latest_release
                ]

                result = await PythonPackageMetadata(
                    package_name, latest_version, package_info, release_info
                )
                self.__class__._cached_packages[
                    f"{package_name}-{latest_version}"
                ] = result
                self.__class__._cached_packages[
                    f"{package_name}-{package_version}"
                ] = result

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
            package = self.__class__._cached_packages.get(
                f"{package_name}-{latest_version}", None
            )
            if package is None:
                await PythonPackageMetadata(
                    package_name, latest_version, package_info, release_info
                )
                self.__class__._cached_packages[
                    f"{package_name}-{latest_version}"
                ] = package

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
        release_info = package_data.get("releases", [[]])[latest_version][
            latest_release
        ]

        result = self.__class__._cached_packages.get(
            f"{package_name}-{latest_version}", None
        )
        if result is None:
            result = PythonPackageMetadata(
                package_name, latest_version, package_info, release_info
            )
            self.__class__._cached_packages[f"{package_name}-{latest_version}"] = result

        return result


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
