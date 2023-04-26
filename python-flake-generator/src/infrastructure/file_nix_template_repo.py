import logging
import os
from pathlib import Path
from typing import Dict, List
import sys

base_folder = str(Path(__file__).resolve().parent.parent)
if base_folder not in sys.path:
    sys.path.append(base_folder)

from domain.flake_recipe import FlakeRecipe
from domain.nix_template_repo import NixTemplateRepo
from domain.nix_template import NixTemplate

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

    def find_flake_templates_by_recipe(self, recipe: FlakeRecipe) -> List[Dict[str, NixTemplate]]:
        """Retrieves the flake templates for given recipe"""
        result = [ ]

        for tmpl_file in Path(sys.modules[recipe.__class__.__module__].__file__).parent.resolve().glob('**/*.tmpl'):
            if tmpl_file.is_file():
                relative_path = tmpl_file.relative_to(Path(self.__class__._recipes_folder)).with_suffix('')
                template = {}
                template["base_folder"] = self.__class__._recipes_folder
                template["folder"] = os.path.dirname(os.path.realpath(tmpl_file))
                template["file"] = str(tmpl_file)
                file_base, file_extension = os.path.splitext(str(tmpl_file))
                template["basename"] = Path(file_base).name
                template["path"] = relative_path
                template["contents"] = self.read_file(tmpl_file)
                result.append(template)
        return result

    def read_file(self, filePath: str) -> str:
        result = ""
        with open(filePath, "r") as file:
            result = file.read()
        return result
