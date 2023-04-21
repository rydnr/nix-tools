from repo import Repo
from resource import Resource


class ResourceRepo(Repo):
    """
    A subclass of Repo that manages resources.
    """
    def __init__(self):
        """
        Creates a new ResourceRepo instance.
        """
        super().__init__(Resource)

    def find_by_path(path: str) -> str:
        """Must be implemented by subclasses"""
        raise NotImplementedError("find_by_path() must be implemented by subclasses")
