import logging
import os
from pathlib import Path
from typing import Dict
import sys

base_folder = str(Path(__file__).resolve().parent.parent)
if base_folder not in sys.path:
    sys.path.append(base_folder)

from domain.flake_nix_template import FlakeNixTemplate
from domain.flake_recipe import FlakeRecipe
from domain.nix_template_repo import NixTemplateRepo
from domain.nix_template import NixTemplate
from domain.package_nix_template import PackageNixTemplate
from infrastructure.resource_files import ResourceFiles

class FileNixTemplateRepo(NixTemplateRepo):
    """
    A NixTemplateRepo using files.
    """

    _recipes_folder = None

    @classmethod
    def recipes_folder(cls, folder: str):
        cls._recipes_folder = folder

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

    def find_flake_templates_by_recipe(self, recipe: FlakeRecipe) -> Dict[str, NixTemplate]:
        """Retrieves the flake templates for given recipe"""
        result = {}
        recipes_folder_path = Path(self.__class__._recipes_folder)
        for tmpl_file in recipes_folder_path.resolve().glob('**/*.tmpl'):
            if tmpl_file.is_file():
                relative_path = tmpl_file.relative_to(recipes_folder_path).with_suffix('')
                result[tmpl_file.stem] = relative_path
        print(f'templates of recipe {recipe} -> {result}')
        return result
