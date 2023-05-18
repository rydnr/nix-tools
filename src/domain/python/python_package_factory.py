from domain.event_emitter import EventEmitter
from domain.event_listener import EventListener
from domain.git.git_repo_found import GitRepoFound
from domain.git.git_repo_requested import GitRepoRequested
from domain.python.python_package import PythonPackage
from domain.python.python_package_created import PythonPackageCreated
from domain.python.unsupported_python_package import UnsupportedPythonPackage

import asyncio
import logging
from typing import Dict, List

class PythonPackageFactory(EventEmitter, EventListener):
    """
    It's responsible for creating PythonPackage instances.
    """
    def __init__(self):
        self._package = None
        self._event = asyncio.Event()

    @classmethod
    def supported_events(cls) -> List:
        return [GitRepoFound]

    async def create(self, name: str, version: str, info: Dict, release: Dict) -> PythonPackage:
        """Creates a PythonPackage matching given name and version."""
        result = None
        logging.getLogger(__name__).debug(f'Waiting for GitRepoFound({name}, {version}) events')
        await self._emit_git_repo_requested(name, version, info, release)
        await self._event.wait()
        return self._package

    async def _emit_git_repo_requested(self, name: str, version: str, info: Dict, release: Dict):
        self.__class__.register_receiver(self)
        await self.__class__.emit(GitRepoRequested(name, version, info, release))

    async def listenGitRepoFound(self, event: GitRepoFound):
        self.__class__.unregister_receiver(self)
        repo_url, subfolder = GitRepo.extract_url_and_subfolder(event.url)
        git_repo = Ports.instance().resolve(GitRepoRepo).find_by_url_and_rev(repo_url, event.version, subfolder=subfolder)

        if not git_repo:
            logging.getLogger(__name__).warn(f'No repository url found for {name}-{version}')
        else:
            for python_package_class in PythonPackage.__subclasses__():
                if python_package_class.git_repo_matches(git_repo):
                    package = python_package_class(name, version, info, release, git_repo)
                    logging.getLogger(__name__).debug(f'Using {python_package_class.__name__} for {git_repo.url}')
                    break

        if not package:
            raise UnsupportedPythonPackage(name, version)

        self._event.set()

        await self.__class__.emit(PythonPackageCreated(package))

    @classmethod
    def old_create(cls, name: str, version: str, info: Dict, release: Dict) -> PythonPackage:
        """Creates a PythonPackage matching given name and version."""
        result = None
        git_repo = PythonPackage.extract_repo(version, info)
        if not git_repo:
            logging.getLogger(__name__).warn(f'No repository url found for {name}-{version}')
        else:
            for python_package_class in PythonPackage.__subclasses__():
                if python_package_class.git_repo_matches(git_repo):
                    result = python_package_class(name, version, info, release, git_repo)
                    logging.getLogger(__name__).debug(f'Using {python_package_class.__name__} for {git_repo.url}')
                    break

        if not result:
            raise UnsupportedPythonPackage(name, version)

        return result
