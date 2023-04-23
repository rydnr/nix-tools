import sys

sys.path.insert(0, "domain")
from flake_repo import FlakeRepo
from flake import Flake
from flake_created_event import FlakeCreated

import logging
from typing import List
import os

class FolderFlakeRepo(FlakeRepo):
    """
    A FlakeRepo using a custom folder.
    """

    _repo_folder = None

    @classmethod
    def repo_folder(cls, folder: str):
        cls._repo_folder = folder

    _flakes_url = None

    @classmethod
    def flakes_url(cls, url: str):
        cls._flakes_url = url

    def __init__(self):
        super().__init__()

    def find_by_name_and_version(self, package_name: str, package_version: str) -> Flake:
        """
        Retrieves the Flake matching given name and version, if any.
        """
        result = None

        if os.path.exists(os.path.join(self.__class__._repo_folder, os.path.join(package_name, f'{package_name}-{package_version}.nix'))):
            # TODO: parse the flake and retrieve the dependencies
            result = Flake(package_name, package_version, None, [], [], [], [])

        return result

    def create(self, flake: Flake, flake_nix: str, flake_nix_path: str, package_nix: str, package_nix_path: str) -> FlakeCreated:
        """Creates the flake"""
        if not os.path.exists(os.path.join(self.__class__._repo_folder, os.path.dirname(flake_nix_path))):
            os.makedirs(os.path.join(self.__class__._repo_folder, os.path.dirname(flake_nix_path)))
        if not os.path.exists(os.path.join(self.__class__._repo_folder, os.path.dirname(package_nix_path))):
            os.makedirs(os.path.join(self.__class__._repo_folder, os.path.dirname(package_nix_path)))

        if os.path.exists(os.path.join(self.__class__._repo_folder, flake_nix_path)):
            return None
        else:
            with open(os.path.join(self.__class__._repo_folder, flake_nix_path), "w") as file:
                file.write(flake_nix)

        if self.find_by_name_and_version(flake.name, flake.version):
            return None
        else:
            with open(os.path.join(self.__class__._repo_folder, package_nix_path), "w") as file:
                file.write(package_nix)

        return FlakeCreated(flake.name, flake.version)

    def url_for_flake(self, name: str, version: str) -> str:
        """Retrieves the url of given flake"""
        return f'{self.__class__._flakes_url}{name}-{version}'
