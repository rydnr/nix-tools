import sys
from pathlib import Path

base_folder = str(Path(__file__).resolve().parent.parent)
if base_folder not in sys.path:
    sys.path.append(base_folder)

from domain.repo import Repo
from domain.nix_template import NixTemplate

class NixTemplateRepo(Repo):
    """
    A subclass of Repo that manages nix templates.
    """

    def __init__(self):
        """
        Creates a new NixTemplateRepo instance.
        """
        super().__init__(NixTemplate)

    def find_flake_template_by_type(self, package_name: str, package_version: str, package_type: str) -> NixTemplate:
        """Retrieves the flake template of given type"""
        raise NotImplementedError(
            "find_flake_template_by_type() must be implemented by subclasses"
        )

    def find_package_template_by_type(self, package_name: str, package_version: str, package_type: str) -> NixTemplate:
        """Retrieves the package template of given type"""
        raise NotImplementedError(
            "find_package_template_by_type() must be implemented by subclasses"
        )
