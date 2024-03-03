# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/git/git_repo_resolver.py

This file defines the GitRepoResolver class.

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
from pythoneda.shared import Event, EventListener
from rydnr.tools.nix.flake.python_generator.git import GitRepo, GitRepoRequested

import asyncio
import logging
from typing import Dict, List, Type


class GitRepoResolver(EventListener):
    """
    Resolves git repositories.
    """

    @classmethod
    def supported_events(cls) -> List[Type[Event]]:
        """
        Retrieves the list of supported event classes.
        """
        return [GitRepoRequested]

    @classmethod
    def fix_url(cls, url: str) -> str:
        result = url
        if result.endswith("/issues"):
            result = result.removesuffix("/issues")
        return result

    @classmethod
    def extract_urls(cls, info: Dict) -> List[str]:
        result = []
        project_urls = info.get("project_urls", {})
        for url in [
            entry["collection"].get(entry["key"], None)
            for entry in [
                {"collection": info, "key": "package_url"},
                {"collection": info, "key": "home_page"},
                {"collection": info, "key": "project_url"},
                {"collection": info, "key": "release_url"},
                {"collection": project_urls, "key": "Source"},
                {"collection": project_urls, "key": "Source Code"},
                {"collection": project_urls, "key": "Home"},
                {"collection": project_urls, "key": "Homepage"},
                {"collection": project_urls, "key": "Changelog"},
                {"collection": project_urls, "key": "Documentation"},
                {"collection": project_urls, "key": "Issue Tracker"},
                {"collection": project_urls, "key": "Tracker"},
            ]
        ]:
            if url:
                result.append(cls.fix_url(url))
        return result

    @classmethod
    async def listenGitRepoRequested(cls, event: GitRepoRequested) -> GitRepo:
        for url in cls.extract_urls(event.info):
            repo_url, subfolder = GitRepo.extract_url_and_subfolder(url)
            if GitRepo.url_is_a_git_repo(repo_url):
                asyncio.ensure_future(
                    cls.emit(
                        GitRepoFound(
                            event.package_name,
                            event.package_version,
                            repo_url,
                            subfolder,
                        )
                    )
                )
                break
        logging.getLogger(__name__).warn(
            f"I couldn't obtain a git repo url from the project's urls"
        )


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
