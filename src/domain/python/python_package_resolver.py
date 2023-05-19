from domain.event import Event
from domain.event_listener import EventListener
from domain.python.python_build_strategy_requested import PythonBuildStrategyRequested
from domain.python.python_package import PythonPackage
from domain.python.python_package_in_progress import PythonPackageInProgress
from domain.python.python_package_requested import PythonPackageRequested
from domain.python.setuppy_strategy_found import SetuppyStrategyFound
from domain.git.git_repo_found import GitRepoFound
from domain.git.git_repo_requested import GitRepoRequested

import asyncio
import logging
from typing import Dict, List, Type


class PythonPackageResolver(EventListener):
    """
    Resolves python packages.
    """

    @classmethod
    def supported_events(cls) -> List[Type[Event]]:
        """
        Retrieves the list of supported event classes.
        """
        return [PythonPackageRequested, GitRepoFound, SetuppyStrategyFound]

    @classmethod
    async def listenPythonPackageRequested(cls, event: PythonPackageRequested):
        logger = logging.getLogger(__name__)
        # 1. annotate the python package as "in-progress"
        metadata = Ports.instance().resolvePythonPackageMetadataRepo().find_by_name_and_version(event.package_name, event.package_version)
        pythonPackageInProgress = PythonPackageInProgress(event.package_name, event.package_version, metadata)
        # 2. emit GitRepoRequested
        self.__class__.emit(GitRepoRequested(metadata.info, metadata.release))

    @classmethod
    async def listenGitRepoFound(cls, event: GitRepoFound):
        logger = logging.getLogger(__name__)
        # 1. retrieve the python project "in-progress"
        # 2. emit PythonBuildStrategyRequested

    @classmethod
    async def listenSetuppyStrategyFound(cls, event: SetuppyStrategyFound):
        logger = logging.getLogger(__name__)
        # 1. instantiate SetuppyPythonProject
        # 2. emit FlakeRequested
