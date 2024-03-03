# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/git/git_repo_repo.py

This file defines the GitRepoRepo class.

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
from pythoneda.shared import Repo
from rydnr.tools.nix.flake.python_generator.git import GitRepo

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
        raise NotImplementedError(
            "find_by_url_and_rev() must be implemented by subclasses"
        )

    def fix_rev(self, url: str, rev: str, subfolder: str) -> str:
        result = None
        owner, repo_name = GitRepo.extract_repo_owner_and_repo_name(url)
        attempts = [rev, f"v{rev}", f"{repo_name}-{rev}", f"{repo_name}_{rev}"]
        if subfolder:
            # Attempting to support monorepos such as `azure-sdk-for-python`
            last_part_of_subfolder = subfolder.split("/")[-1]
            attempts.append(f"{last_part_of_subfolder}_{rev}")
            attempts.append(f"{last_part_of_subfolder}-{rev}")

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


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
