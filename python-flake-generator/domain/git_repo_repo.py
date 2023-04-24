import sys
from pathlib import Path

base_folder = str(Path(__file__).resolve().parent.parent)
if base_folder not in sys.path:
    sys.path.append(base_folder)

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
        """Must be implemented by subclasses"""
        raise NotImplementedError("find_by_url() must be implemented by subclasses")

    def repo_sha256(self, repo: GitRepo):
        # Use nix-prefetch-git to compute the hash
        result = subprocess.run(['nix-prefetch-git', '--deepClone', f'{repo.url}/tree/{repo.rev}'], check=True, capture_output=True, text=True)
        output = result.stdout
        logging.getLogger(__name__).debug(f'nix-prefetch-git --deepClone {repo.url}/tree/{repo.rev} -> {output}')

        return output.splitlines()[-1]
