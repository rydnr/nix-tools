from repo import Repo
from git_repo import GitRepo

from typing import Dict


class GitRepoRepo(Repo):
    """
    A subclass of Repo that manages Git repositories.
    """

    def __init__(self):
        """
        Creates a new GitRepoRepo instance.
        """
        super().__init__(GitRepo)

    def find_by_url_and_rev(self, url: str, revision: str) -> Dict[str, str]:
        """Must be implemented by subclasses"""
        raise NotImplementedError("find_by_url() must be implemented by subclasses")
