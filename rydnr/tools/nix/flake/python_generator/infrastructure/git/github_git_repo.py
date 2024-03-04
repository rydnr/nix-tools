# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/infrastructure/git/github_git_repo.py

This file defines the GithubGitRepo class.

Copyright (C) 2023-today rydnr's rydnr/python-nix-flake-generator

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from rydnr.tools.nix.flake.python_generator.git.git_repo import GitRepo
from rydnr.tools.nix.flake.python_generator.git.git_repo_repo import GitRepoRepo
from rydnr.tools.nix.flake.python_generator.infrastructure.git.github_repo import (
    GithubRepo,
)

import requests


class GithubGitRepo(GitRepoRepo):
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
        repo_info = requests.get(
            f"https://api.github.com/repos/{owner}/{repo_name}", headers=headers
        ).json()

        return GithubRepo(
            url, tag, repo_info, self.__class__._github_token, subfolder=subfolder
        )

    def revision_exists(self, url: str, rev: str) -> bool:
        headers = {
            "Authorization": f"token {self.__class__._github_token}",
            "Accept": "application/vnd.github+json",
        }

        owner, repo_name = GitRepo.extract_repo_owner_and_repo_name(url)
        response = requests.get(
            f"https://api.github.com/repos/{owner}/{repo_name}/git/refs/tags/{rev}",
            headers=headers,
        )

        return response.status_code == 200

    def get_latest_tag(self, url: str) -> str:
        result = None
        owner, repo_name = GitRepo.extract_repo_owner_and_repo_name(url)

        headers = {"Authorization": f"token {self.__class__._github_token}"}
        tagInfo = requests.get(
            f"https://api.github.com/repos/{owner}/{repo_name}/tags", headers=headers
        ).json()

        if tagInfo and len(tagInfo) > 0:
            result = tagInfo[0]["name"]

        return result


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
