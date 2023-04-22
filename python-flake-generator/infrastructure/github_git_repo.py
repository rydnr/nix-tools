#!/usr/bin/env python3

from git_repo_repo import GitRepoRepo
from git_repo import GitRepo
#from description import extract_description
#from nix import get_nix_prefetch_git_hash
import re
import requests
import base64
from typing import Dict

class GithubGitRepo(GitRepoRepo):

    """
    A GitRepo that uses Github as store
    """
    def __init__(self):
        super().__init__()

    _github_token = None

    @classmethod
    def github_token(cls, token: str):
        cls._github_token = token

    def find_by_url_and_rev(self, url: str, rev: str) -> GitRepo:
        if not url:
            return None

        if not self.revision_exists(url, rev):
            rev = f'v{rev}'

        if not self.revision_exists(url, rev):
            return None

        owner, repo_name = self.extract_owner_and_repo_name(url)
        headers = {"Authorization": f"token {self.__class__._github_token}"}
        repo_info = requests.get(f"https://api.github.com/repos/{owner}/{repo_name}", headers=headers).json()
        pyproject_toml = self.get_file_contents_in_github_repo(url, rev, "pyproject.toml")
        pipfile = self.get_file_contents_in_github_repo(url, rev, "Pipfile")
        poetry_lock = self.get_file_contents_in_github_repo(url, rev, "poetry.lock")

        return GitRepo(url, rev, repo_info, { "pyproject.toml": pyproject_toml, "Pipfile": pipfile, "poetry.lock": poetry_lock })

    def revision_exists(self, url: str, rev: str) -> bool:
        headers = {"Authorization": f"token {self.__class__._github_token}", "Accept": "application/vnd.github+json"}

        owner, repo_name = self.extract_owner_and_repo_name(url)
        response = requests.get(f"https://api.github.com/repos/{owner}/{repo_name}/git/refs/tags/{rev}", headers=headers)

        return response.status_code == 200

    def extract_owner_and_repo_name(self, url: str) -> tuple:
        pattern = r"(?:https?://)?(?:www\.)?github\.com/([^/]+)/([^/]+)"
        try:
            match = re.match(pattern, url)
            owner, repo_name = match.groups()
            return owner, repo_name

        except:
            print(f"Invalid repo: {url}")

    def request_file_in_github_repo(self, url: str, rev: str, file: str) -> bool:
        headers = {"Authorization": f"token {self.__class__._github_token}", "Accept": "application/vnd.github+json"}

        owner, repo_name = self.extract_owner_and_repo_name(url)
        return requests.get(f"https://api.github.com/repos/{owner}/{repo_name}/contents/{file}?ref={rev}", headers=headers)

    def file_exists_in_github_repo(self, url: str, rev: str, file: str) -> bool:
        file_info = self.request_file_in_github_repo(url, rev, file)

        return file_info.status_code == 200

    def get_file_contents_in_github_repo(self, url: str, rev: str, file: str) -> str:
        file_info = self.request_file_in_github_repo(url, rev, file)

        if (file_info.status_code == 200):
            decoded_bytes = base64.b64decode(file_info.json().get("content", ""))
            return decoded_bytes.decode('utf-8')
        else:
            return ""
