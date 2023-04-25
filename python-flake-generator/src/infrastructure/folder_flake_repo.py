import sys
from pathlib import Path

base_folder = str(Path(__file__).resolve().parent.parent)
if base_folder not in sys.path:
    sys.path.append(base_folder)

from domain.flake_repo import FlakeRepo
from domain.flake import Flake
from domain.flake_created_event import FlakeCreated

import logging
from typing import Dict, List
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

    def find_by_name_and_version(self, package_name: str, package_version: str) -> Flake:
        """
        Retrieves the Flake matching given name and version, if any.
        """
        result = None

        if os.path.exists(os.path.join(self.__class__._repo_folder, os.path.join(package_name, f'{package_name}-{package_version}.nix'))):
            # TODO: parse the flake and retrieve the dependencies
            result = Flake(package_name, package_version, None, [], [], [], [])

        return result

    def create(self, flake: Flake, content: List[Dict[str, str]]) -> FlakeCreated:
#    def create(self, flake: Flake, flake_nix: str, flake_nix_path: str, package_nix: str, package_nix_path: str) -> FlakeCreated:
        """Creates the flake"""
        if self.find_by_name_and_version(flake.name, flake.version):
            return None

        for item in content:
            if os.path.exists(os.path.join(self.__class__._repo_folder, item["path"])):
                return None

            if not os.path.exists(os.path.join(self.__class__._repo_folder, os.path.dirname(item["path"]))):
                os.makedirs(os.path.join(self.__class__._repo_folder, os.path.dirname(item["path"])))

            with open(os.path.join(self.__class__._repo_folder, item["path"]), "w") as file:
                file.write(item["contents"])

        return FlakeCreated(flake.name, flake.version)

    def url_for_flake(self, name: str, version: str) -> str:
        """Retrieves the url of given flake"""
        return f'{self.__class__._flakes_url}{name}-{version}'

import traceback

def print_stack_trace():
    stack_trace = traceback.format_stack()
    print("".join(stack_trace))
