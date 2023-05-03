from domain.entity import Entity, attribute
from domain.error_cloning_git_repository import ErrorCloningGitRepository
from domain.git_checkout_failed import GitCheckoutFailed

import logging
import os
import re
import subprocess
from urllib.parse import urlparse
from typing import Dict

class GitRepo(Entity):
    """
    Represents a Git repository.
    """
    def __init__(self, url: str, rev: str, repo_info: Dict, subfolder=None):
        """Creates a new Git repository instance"""
        super().__init__(id)
        self._url = url
        self._rev = rev
        self._repo_info = repo_info
        self._subfolder = subfolder
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

    @property
    @attribute
    def subfolder(self):
        return self._subfolder

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

    def clone(self, folder: str, subfolder: str):
        result = os.path.join(folder, subfolder)

        try:
            subprocess.run(['git', 'clone', self.url, subfolder], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=folder)
        except subprocess.CalledProcessError as err:
            logging.getLogger(__name__).error(err.stdout)
            logging.getLogger(__name__).error(err.stderr)
            raise ErrorCloningGitRepository(self.url, folder)
        try:
            subprocess.run(['git', 'checkout', self.rev], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=result)
        except subprocess.CalledProcessError as err:
            logging.getLogger(__name__).error(err.stdout)
            logging.getLogger(__name__).error(err.stderr)
            raise GitCheckoutFailed(self.url, self.rev, folder)

        return result

    @classmethod
    def extract_url_and_subfolder(cls, url: str) -> tuple:
        parsed_url = urlparse(url)
        path_parts = parsed_url.path.split('/')

        if len(path_parts) > 4 and path_parts[3] == 'tree':
            repo_url = f"{parsed_url.scheme}://{parsed_url.netloc}/{path_parts[1]}/{path_parts[2]}"
            subfolder = '/'.join(path_parts[5:])
        else:
            repo_url = f"{parsed_url.scheme}://{parsed_url.netloc}/{path_parts[1]}/{path_parts[2]}"
            subfolder = '/'.join(path_parts[3:])

        return repo_url, subfolder
