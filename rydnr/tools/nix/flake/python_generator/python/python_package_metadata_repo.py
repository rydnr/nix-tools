# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/python/python_package_metadata_repo.py

This file defines the PythonPackageMetadataRepo class.

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
from .python_package_metadata import PythonPackageMetadata
from pythoneda.shared import Repo

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

    async def find_by_name_and_version(
        self, package_name: str, version_spec: str
    ) -> PythonPackageMetadata:
        """Retrieves the metadata of the PythonPackage matching given name and version."""
        raise NotImplementedError(
            "find_by_name_and_version() must be implemented by subclasses"
        )

    async def find_by_name(self, package_name: str) -> PythonPackageMetadata:
        """Retrieves the metadata of the latest version of the PythonPackage matching given name."""
        raise NotImplementedError("find_by_name() must be implemented by subclasses")

    async def find_all_by_name(self, package_name: str) -> List[PythonPackageMetadata]:
        """Retrieves the metadata for all versions of the PythonPackage matching given name."""
        raise NotImplementedError(
            "find_all_by_name() must be implemented by subclasses"
        )


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
