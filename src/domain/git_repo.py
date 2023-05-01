from domain.entity import Entity, attribute

import logging
import re
import subprocess
from typing import Dict

class GitRepo(Entity):
    """
    Represents a Git repository.
    """
    def __init__(self, url: str, rev: str, repo_info: Dict):
        """Creates a new Git repository instance"""
        super().__init__(id)
        self._url = url
        self._rev = rev
        self._repo_info = repo_info
        self._files = {}

    @property
    @attribute
    def url(self):
        return self._url

    @property
    @attribute
    def rev(self):
        return self._rev

    @property
    @attribute
    def repo_info(self):
        return self._repo_info

    def get_file(self, fileName: str) -> str:
        """
        Retrieves the contents of given file in the repo.
        """
        result = self._files.get(fileName, None)
        if not result:
            result = self.access_file(fileName)
            self._files[fileName] = result

        return result

    def access_file(self, fileName: str) -> str:
        """
        Retrieves the contents of given file in the repo
        """
        raise NotImplementedError("access_file() must be implemented by subclasses")

    def repo_owner_and_repo_name(self) -> tuple:
        return self.__class__.extract_repo_owner_and_repo_name(self.url)

    @classmethod
    def url_is_a_git_repo(cls, url: str) -> bool:
        try:
            subprocess.check_output(['git', 'ls-remote', url], stderr=subprocess.STDOUT)
            return True
        except subprocess.CalledProcessError:
            return False

    @classmethod
    def extract_repo_owner_and_repo_name(cls, url: str) -> tuple:
        pattern = r"(?:https?://)?(?:www\.)?.*\.com/([^/]+)/([^/]+)"
        try:
            match = re.match(pattern, url)
            owner, repo_name = match.groups()
            return owner, repo_name

        except:
            logging.getLogger(cls.__name__).error(f"Invalid repo: {url}")

    def sha256(self):
        # Use nix-prefetch-git to compute the hash
        result = subprocess.run(['nix-prefetch-git', '--deepClone', f'{self.url}/tree/{self.rev}'], check=True, capture_output=True, text=True)
        output = result.stdout
        logging.getLogger(__name__).debug(f'nix-prefetch-git --deepClone {self.url}/tree/{self.rev} -> {output}')

        return output.splitlines()[-1]
