
from domain.flake import Flake
from domain.flake_created import FlakeCreated
from domain.flake_recipe import FlakeRecipe
from domain.flake_repo import FlakeRepo

import logging
import os
from typing import Dict, List

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

    def flake_folder(self, package_name: str, package_version: str) -> str:
        return os.path.join(self.__class__._repo_folder, f'{package_name}-{package_version}')

    def flake_nix_path(self, package_name: str, package_version: str) -> str:
        return os.path.join(self.flake_folder(package_name, package_version), 'flake.nix')

    def find_by_name_and_version(self, package_name: str, package_version: str) -> Flake:
        """
        Retrieves the Flake matching given name and version, if any.
        """
        result = None

        if os.path.exists(self.flake_nix_path(package_name, package_version)):
            # TODO: parse the flake and retrieve the dependencies
            result = Flake(package_name, package_version, None, [], [], [], [], [])

        return result

    def create(self, flake: Flake, content: List[Dict[str, str]], recipe: FlakeRecipe) -> FlakeCreated:
#    def create(self, flake: Flake, flake_nix: str, flake_nix_path: str, package_nix: str, package_nix_path: str) -> FlakeCreated:
        """Creates the flake"""
        if self.find_by_name_and_version(flake.name, flake.version):
            logging.getLogger(__name__).warning(f'Not creating flake {flake.name}-{flake.version} since it already exists')
            return None

        for item in content:
            if os.path.exists(os.path.join(self.__class__._repo_folder, item["path"])):
                logging.getLogger(__name__).debug(f'Not overwriting {item["path"]} in {self.__class__._repo_folder}')
            else:
                if not os.path.exists(os.path.join(self.__class__._repo_folder, os.path.dirname(item["path"]))):
                    os.makedirs(os.path.join(self.__class__._repo_folder, os.path.dirname(item["path"])))

                with open(os.path.join(self.__class__._repo_folder, item["path"]), "w") as file:
                    logging.getLogger(__name__).debug(f'Writing {item["path"]}')
                    file.write(item["contents"])

        return FlakeCreated(flake.name, flake.version, self.flake_folder(flake.name, flake.version), recipe)

    def url_for_flake(self, name: str, version: str) -> str:
        """Retrieves the url of given flake"""
        return f'{self.__class__._flakes_url}{name}-{version}'
