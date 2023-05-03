from domain.git_repo_repo import GitRepoRepo
from domain.git_repo import GitRepo
from infrastructure.github_repo import GithubRepo

import requests

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

    def find_by_url_and_rev(self, url: str, rev: str, subfolder=None) -> GitRepo:
        if not url:
            return None

        tag = self.fix_rev(url, rev, subfolder)

        owner, repo_name = GitRepo.extract_repo_owner_and_repo_name(url)

        headers = {"Authorization": f"token {self.__class__._github_token}"}
        repo_info = requests.get(f"https://api.github.com/repos/{owner}/{repo_name}", headers=headers).json()

        return GithubRepo(url, tag, repo_info, self.__class__._github_token, subfolder=subfolder)

    def revision_exists(self, url: str, rev: str) -> bool:
        headers = {"Authorization": f"token {self.__class__._github_token}", "Accept": "application/vnd.github+json"}

        owner, repo_name = GitRepo.extract_repo_owner_and_repo_name(url)
        response = requests.get(f"https://api.github.com/repos/{owner}/{repo_name}/git/refs/tags/{rev}", headers=headers)

        return response.status_code == 200
