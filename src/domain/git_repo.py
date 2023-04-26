from domain.entity import Entity, attribute

import re
import subprocess
from typing import Dict

class GitRepo(Entity):
    """
    Represents a Git repository.
    """
    def __init__(self, url: str, rev: str, repo_info: Dict, files: Dict[str, str]):
        """Creates a new Git repository instance"""
        super().__init__(id)
        self._url = url
        self._rev = rev
        self._repo_info = repo_info
        self._files = files

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

    @property
    @attribute
    def files(self):
        return self._files

    def pyproject_toml(self):
        return self._files.get("pyproject.toml", None)

    def pipfile(self):
        return self._files.get("Pipfile", None)

    def poetry_lock(self):
        return self._files.get("poetry.lock", None)

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
