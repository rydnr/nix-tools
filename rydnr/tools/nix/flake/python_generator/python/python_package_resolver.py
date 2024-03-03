# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/python/python_package_resolver.py

This file defines the PythonPackageResolver class.

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
from domain.event import Event
from domain.event_emitter import EventEmitter
from domain.event_listener import EventListener
from domain.python.build.python_build_strategy_requested import (
    PythonBuildStrategyRequested,
)
from domain.python.build.setuppy_strategy_found import SetuppyStrategyFound
from domain.python.python_package import PythonPackage
from domain.python.python_package_in_progress import PythonPackageInProgress
from domain.python.python_package_requested import PythonPackageRequested
from domain.python.python_package_resolved import PythonPackageResolved
from domain.git.git_repo import GitRepo
from domain.git.git_repo_found import GitRepoFound
from domain.git.git_repo_requested import GitRepoRequested
from domain.nix.python.nix_python_package_in_nixpkgs import NixPythonPackageInNixpkgs


import logging
from typing import Dict, List, Type


class PythonPackageResolver(EventListener, EventEmitter):
    """
    Resolves python packages.
    """

    @classmethod
    def supported_events(cls) -> List[Type[Event]]:
        """
        Retrieves the list of supported event classes.
        """
        return [
            PythonPackageRequested,
            GitRepoFound,
            SetuppyStrategyFound,
            NixPythonPackageInNixpkgs,
        ]

    @classmethod
    async def listenPythonPackageRequested(cls, event: PythonPackageRequested):
        logger = logging.getLogger(__name__)
        # 1. annotate the python package as "in-progress"
        metadata = (
            Ports.instance()
            .resolvePythonPackageMetadataRepo()
            .find_by_name_and_version(event.package_name, event.package_version)
        )
        pythonPackageInProgress = PythonPackageInProgress(
            event.package_name, event.package_version, metadata
        )
        # 2. emit GitRepoRequested
        await self.__class__.emit(GitRepoRequested(metadata.info, metadata.release))

    @classmethod
    async def listenGitRepoFound(cls, event: GitRepoFound):
        logger = logging.getLogger(__name__)
        # 1. retrieve the python project "in-progress"
        pythonPackageInProgress = PythonPackageInProgress.matching(
            name=event.package_name, version=event.package_version
        )
        if pythonPackageInProgress:
            # 2. emit PythonBuildStrategyRequested
            await self.__class__.emit(
                PythonBuildStrategyRequested(
                    event.package_name,
                    event.package_version,
                    GitRepo(
                        event.url, event.tag, event.metadata, subfolder=event.subfolder
                    ),
                )
            )

    @classmethod
    async def listenSetuppyStrategyFound(cls, event: SetuppyStrategyFound):
        logger = logging.getLogger(__name__)
        pythonPackage = SetuppyPythonPackage(
            event.package_name,
            event.package_version,
            event.pythonPackage.info,
            event.pythonPackage.release,
            event.pythonPackage.git_repo,
        )
        # 2. emit PythonPackageRequested for each dependency
        for dep in list(
            set(pythonPackage.native_build_inputs)
            | set(pythonPackage.propagated_build_inputs)
            | set(pythonPackage.build_inputs)
            | set(pythonPackage.check_inputs)
            | set(pythonPackage.optional_inputs)
        ):
            pythonPackageInProgress = PythonPackageInProgress(dep.name, dep.version)
            await self.__class__.emit(PythonPackageRequested(dep.name, dep.version))
        await self.__class__.emit(
            PythonPackageResolved(dep.name, dep.version, pythonPackage)
        )

    @classmethod
    async def listenNixPythonPackageInNixpkgs(cls, event: NixPythonPackageInNixpkgs):
        pythonPackageInProgress = PythonPackageInProgress.matching(
            name=event.python_package.package_name,
            version=event.python_package.package_version,
        )


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
