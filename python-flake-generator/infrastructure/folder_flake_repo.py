import sys

sys.path.insert(0, "domain")
from flake_repo import FlakeRepo
from flake import Flake

import logging
from typing import List


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
        print(f'folder: {self.__class__._repo_folder}, url: {self.__class__._flakes_url}')
        return None
