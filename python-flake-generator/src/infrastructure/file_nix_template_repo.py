import sys
from pathlib import Path

base_folder = str(Path(__file__).resolve().parent.parent)
if base_folder not in sys.path:
    sys.path.append(base_folder)

from domain.nix_template_repo import NixTemplateRepo
from domain.nix_template import NixTemplate
from domain.flake_nix_template import FlakeNixTemplate
from domain.package_nix_template import PackageNixTemplate
from infrastructure.resource_files import ResourceFiles

import logging
import os
from typing import Dict

class FileNixTemplateRepo(NixTemplateRepo):
    """
    A NixTemplateRepo using files.
    """

    def __init__(self):
        super().__init__()

    def flake_nix_setuptools_template(self, package_name: str, package_version: str) -> Dict[str, str]:
        return { "contents": ResourceFiles.instance().read_resource_file(os.path.join("setuptools", "flake.nix.tmpl")),
                 "folder": f"{package_name}-{package_version}",
                 "path": "flake.nix" }

    def flake_nix_poetry_template(self, package_name: str, package_version: str) -> Dict[str, str]:
        return { "contents": ResourceFiles.instance().read_resource_file(os.path.join("poetry", "flake.nix.tmpl")),
                 "folder": f"{package_name}-{package_version}",
                 "path": "flake.nix" }

    def resolve_flake_nix_template(self, package_name: str, package_version: str, package_type: str) -> Dict[str, str]:
        mapping = {
            "poetry": self.flake_nix_poetry_template,
            "setuptools": self.flake_nix_setuptools_template
        }

        result = mapping.get(package_type, None)
        if not result:
            result = self.flake_nix_setuptools_template

        return result(package_name, package_version)

    def package_nix_setuptools_pypi_template(self, package_name: str, package_version: str) -> str:
        return { "contents": ResourceFiles.instance().read_resource_file(os.path.join("setuptools", "pypi", "package.nix.tmpl")),
                 "folder": f"{package_name}-{package_version}",
                 "path": f"{package_name}-{package_version}.nix" }

    def package_nix_setuptools_github_template(self, package_name: str, package_version: str) -> str:
        return { "contents": ResourceFiles.instance().read_resource_file(os.path.join("setuptools", "github", "package.nix.tmpl")),
                 "folder": f"{package_name}-{package_version}",
                 "path": f"{package_name}-{package_version}.nix" }

    def package_nix_poetry_template(self, package_name: str, package_version: str) -> str:
        return { "contents": ResourceFiles.instance().read_resource_file(os.path.join("poetry", "package.nix.tmpl")),
                 "folder": f"{package_name}-{package_version}",
                 "path": f"{package_name}-{package_version}.nix" }

    def resolve_package_nix_template(self, package_name: str, package_version: str, package_type: str) -> str:
        mapping = {
            "poetry": self.package_nix_poetry_template,
            "setuptools": self.package_nix_setuptools_github_template
        }
        result = mapping.get(package_type, None)
        if not result:
            result = self.package_nix_setuptools_github_template

        return result(package_name, package_version)

    def find_flake_template_by_type(self, package_name: str, package_version: str, package_type: str) -> NixTemplate:
        """Retrieves the flake template of given type"""
        metadata = self.resolve_flake_nix_template(package_name, package_version, package_type)
        return FlakeNixTemplate(metadata["folder"], metadata["path"], metadata["contents"])

    def find_package_template_by_type(self, package_name: str, package_version: str, package_type: str) -> NixTemplate:
        """Retrieves the package template of given type"""
        metadata = self.resolve_package_nix_template(package_name, package_version, package_type)
        return PackageNixTemplate(metadata["folder"], metadata["path"], metadata["contents"])
