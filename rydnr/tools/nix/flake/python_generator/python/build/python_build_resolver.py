from domain.event import Event
from domain.event_emitter import EventEmitter
from domain.event_listener import EventListener
from domain.python.build.python_build_strategy_requested import PythonBuildStrategyRequested
from domain.python.python_package import PythonPackage
from domain.python.python_package_in_progress import PythonPackageInProgress

import logging
from typing import List, Type


class PythonBuildResolver(EventListener, EventEmitter):
    """
    Resolves python packages.
    """

    @classmethod
    def supported_events(cls) -> List[Type[Event]]:
        """
        Retrieves the list of supported event classes.
        """
        return [PythonBuildStrategyRequested]

    @classmethod
    async def listenPythonBuildStrategyRequested(cls, event: PythonBuildStrategyRequested):
        logger = logging.getLogger(__name__)
        package = None
        pythonPackageInProgress = PythonPackageInProgress(event.package_name, event.package_version, metadata)
        for python_package_class in PythonPackage.__subclasses__():
            if python_package_class.git_repo_matches(git_repo):
                package = python_package_class(event.package_name, event.package_version, pythonPackageInProgress.metadata, event.git_repo)
                logging.getLogger(__name__).debug(f'Using {python_package_class.__name__} for {event.git_repo.url}')
                break

        if package:
            self.__class__.emit(package.build_strategy_event())
