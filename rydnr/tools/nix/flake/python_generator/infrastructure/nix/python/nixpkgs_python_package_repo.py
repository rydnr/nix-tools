# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/infrastructure/nix/python/nixpkgs_python_package_repo.py

This file defines the NixpkgsPythonPackageRepo   class.

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
from rydnr.tools.nix.flake.python_generator.nix.python.nix_python_package import (
    NixPythonPackage,
)
from rydnr.tools.nix.flake.python_generator.nix.python.nix_python_package_repo import (
    NixPythonPackageRepo,
)

import ast
import json
import logging
import subprocess
from typing import List


def get_python3_packages() -> List[NixPythonPackage]:
    """
    Retrieves the NixPythonPackages matching given name.
    """
    result = []

    try:
        cmd = f"nix-instantiate --eval -E 'with import <nixpkgs> {{}}; builtins.toJSON (builtins.map (name: {{ inherit name; version = (builtins.tryEval (python3Packages.${{name}}.version or null)).value; }}) (builtins.attrNames python3Packages))'"

        output = subprocess.check_output(cmd, shell=True)
        output_str = output.decode("utf-8").strip()
        json_str = ast.literal_eval(output_str)
        all_packages = json.loads(json_str)

        for package in all_packages:
            result.append(NixPythonPackage(package["name"], package["version"]))
    except subprocess.CalledProcessError:
        return []

    return result


python3Packages = get_python3_packages()


class NixpkgsPythonPackageRepo(NixPythonPackageRepo):
    """
    A NixPythonPackageRepo on top of nixpkgs
    """

    def __init__(self):
        super().__init__()

    async def find_by_name(self, package_name: str) -> List[NixPythonPackage]:
        """
        Retrieves the NixPythonPackages matching given name.
        """
        result = []

        try:
            lower_package = package_name.lower()
            packages = [
                pkg for pkg in python3Packages if lower_package == pkg.name.lower()
            ]

            for package in packages:
                result.append(package)
        except subprocess.CalledProcessError:
            return []

        return result

    async def find_by_name_and_version(
        self, package_name: str, package_version: str
    ) -> NixPythonPackage:
        """
        Retrieves the NixPythonPackages matching given name and version.
        """
        matches = [
            p
            for p in await self.find_by_name(package_name)
            if p.is_compatible_with(package_version)
        ]
        if len(matches) > 0:
            return matches[0]
        else:
            return None


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
