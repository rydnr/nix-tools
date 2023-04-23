import sys

sys.path.insert(0, "domain")
from nix_python_package_repo import NixPythonPackageRepo
from nix_python_package import NixPythonPackage

import logging
import subprocess
import json
import ast
from typing import List

def get_python3_packages() -> List[NixPythonPackage]:
    """
    Retrieves the NixPythonPackages matching given name.
    """
    result = []

    try:
        cmd = f'nix-instantiate --eval -E \'with import <nixpkgs> {{}}; builtins.toJSON (builtins.map (name: {{ inherit name; version = (builtins.tryEval (python3Packages.${{name}}.version or null)).value; }}) (builtins.attrNames python3Packages))\''

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

    def find_by_name(self, package_name: str) -> List[NixPythonPackage]:
        """
        Retrieves the NixPythonPackages matching given name.
        """
        result = []
        logging.debug(f"looking for {package_name} in nixpkgs")

        try:
            lower_package = package_name.lower()
            packages = [pkg for pkg in python3Packages if lower_package == pkg.name.lower()]

            for package in packages:
                result.append(package)
        except subprocess.CalledProcessError:
            return []

        return result

    def find_by_name_and_version(self, package_name: str, package_version: str) -> NixPythonPackage:
        """
        Retrieves the NixPythonPackages matching given name and version.
        """
        matches = [p for p in self.find_by_name(package_name) if p.version == package_version]
        if len(matches) > 0:
            return matches[0]
        else:
            return None
