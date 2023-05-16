from domain.event import Event
from domain.event_listener import EventListener
from domain.git_repo import GitRepo
from domain.git_repo_requested import GitRepoRequested

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
        return [ GitRepoRequested ]

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
                asyncio.ensure_future(cls.emit(
                    GitRepoFound(
                        event.package_name, event.package_version, repo_url, subfolder
                    )
                ))
                break
        logging.getLogger(__name__).warn(
            f"I couldn't obtain a git repo url from the project's urls"
        )

