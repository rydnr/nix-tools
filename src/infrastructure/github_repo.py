from domain.git_repo import GitRepo

import base64
import requests
from typing import Dict

class GithubRepo(GitRepo):
    def __init__(self, url: str, rev: str, repoInfo: Dict, githubToken: str, subfolder=None):
        """Creates a new Git repository instance"""
        super().__init__(url, rev, repoInfo, subfolder=subfolder)
        self._github_token = githubToken

    def access_file(self, fileName: str) -> str:
        """
        Retrieves the contents of given file in the repo
        """
        return self.get_file_contents_in_github_repo(self.url, self.rev, self.subfolder, fileName)

    def get_file_contents_in_github_repo(self, url: str, rev: str, subfolder: str, file: str) -> str:
        file_info = self.request_file_in_github_repo(url, rev, subfolder, file)

        if (file_info.status_code == 200):
            decoded_bytes = base64.b64decode(file_info.json().get("content", ""))
            return decoded_bytes.decode('utf-8')
        else:
            return None

    def request_file_in_github_repo(self, url: str, rev: str, subfolder: str, file: str) -> bool:
        headers = {"Authorization": f"token {self._github_token}", "Accept": "application/vnd.github+json"}

        owner, repo_name = GitRepo.extract_repo_owner_and_repo_name(url)
        if subfolder:
            final_file = f'{subfolder}/{file}'
        else:
            final_file = file

        return requests.get(f"https://api.github.com/repos/{owner}/{repo_name}/contents/{final_file}?ref={rev}", headers=headers)

    def file_exists_in_github_repo(self, url: str, rev: str, subfolder: str, file: str) -> bool:
        file_info = self.request_file_in_github_repo(url, rev, subfolder, file)

        return file_info.status_code == 200
