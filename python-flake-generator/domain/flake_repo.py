import sys
from pathlib import Path

base_folder = str(Path(__file__).resolve().parent.parent)
if base_folder not in sys.path:
    sys.path.append(base_folder)

from domain.repo import Repo
from domain.flake import Flake
from domain.flake_created_event import FlakeCreated

from typing import Dict, List

class FlakeRepo(Repo):
    """
    A subclass of Repo that manages Flakes.
    """

    def __init__(self):
        """
        Creates a new FlakeRepo instance.
        """
        super().__init__(Flake)

    def find_by_name_and_version(self, name: str, version: str) -> Flake:
        """Retrieves a flake matching given name and version"""
        raise NotImplementedError("find_by_name_and_version() must be implemented by subclasses")

    def create(self, flake: Flake, content: List[Dict[str, str]]) -> FlakeCreated:
        """Creates the flake"""
        raise NotImplementedError("create() must be implemented by subclasses")

    def url_for_flake(self, name: str, version: str) -> str:
        """Retrieves the url of given flake"""
        raise NotImplementedError("url_for_flake() must be implemented by subclasses")
