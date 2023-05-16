from domain.repo import Repo
from domain.git_repo import GitRepo

from typing import Dict
import logging
import subprocess

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
        """Retrieves the git repository for given url and revision."""
        raise NotImplementedError("find_by_url_and_rev() must be implemented by subclasses")

    def fix_rev(self, url: str, rev: str, subfolder: str) -> str:
        result = None
        owner, repo_name = GitRepo.extract_repo_owner_and_repo_name(url)
        attempts = [ rev, f'v{rev}', f'{repo_name}-{rev}', f'{repo_name}_{rev}' ]
        if subfolder:
            # Attempting to support monorepos such as `azure-sdk-for-python`
            last_part_of_subfolder = subfolder.split('/')[-1]
            attempts.append(f'{last_part_of_subfolder}_{rev}')
            attempts.append(f'{last_part_of_subfolder}-{rev}')

        for tag in attempts:
            if self.revision_exists(url, tag):
                result = tag
                break

        if not result:
            result = self.get_latest_tag(url)

        return result

    def get_latest_tag(self, user, repo):
        """Retrieves the git repository for given url and revision."""
        raise NotImplementedError("get_latest_tag() must be implemented by subclasses")
