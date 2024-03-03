# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/infrastructure/git/github_repo.py

This file defines the GithubRepo class.

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
from domain.git.git_repo import GitRepo

import base64
import requests
from typing import Dict


class GithubRepo(GitRepo):
    def __init__(
        self, url: str, rev: str, repoInfo: Dict, githubToken: str, subfolder=None
    ):
        """Creates a new Git repository instance"""
        super().__init__(url, rev, repoInfo, subfolder=subfolder)
        self._github_token = githubToken

    def access_file(self, fileName: str) -> str:
        """
        Retrieves the contents of given file in the repo
        """
        return self.get_file_contents_in_github_repo(
            self.url, self.rev, self.subfolder, fileName
        )

    def get_file_contents_in_github_repo(
        self, url: str, rev: str, subfolder: str, file: str
    ) -> str:
        file_info = self.request_file_in_github_repo(url, rev, subfolder, file)

        if file_info.status_code == 200:
            decoded_bytes = base64.b64decode(file_info.json().get("content", ""))
            return decoded_bytes.decode("utf-8")
        else:
            return None

    def request_file_in_github_repo(
        self, url: str, rev: str, subfolder: str, file: str
    ) -> bool:
        headers = {
            "Authorization": f"token {self._github_token}",
            "Accept": "application/vnd.github+json",
        }

        owner, repo_name = GitRepo.extract_repo_owner_and_repo_name(url)
        if subfolder:
            final_file = f"{subfolder}/{file}"
        else:
            final_file = file

        return requests.get(
            f"https://api.github.com/repos/{owner}/{repo_name}/contents/{final_file}?ref={rev}",
            headers=headers,
        )

    def file_exists_in_github_repo(
        self, url: str, rev: str, subfolder: str, file: str
    ) -> bool:
        file_info = self.request_file_in_github_repo(url, rev, subfolder, file)

        return file_info.status_code == 200


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
