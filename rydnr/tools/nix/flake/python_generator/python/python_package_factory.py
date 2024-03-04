# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/python/python_package_factory.py

This file defines the PythonPackageFactory class.

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
from pythoneda.shared import EventEmitter, EventListener
from rydnr.tools.nix.flake.python_generator.git.git_repo_found import GitRepoFound
from rydnr.tools.nix.flake.python_generator.git.git_repo_requested import (
    GitRepoRequested,
)
from rydnr.tools.nix.flake.python_generator.python.python_package import PythonPackage
from rydnr.tools.nix.flake.python_generator.python.python_package_created import (
    PythonPackageCreated,
)
from rydnr.tools.nix.flake.python_generator.python.unsupported_python_package import (
    UnsupportedPythonPackage,
)

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

    async def create(
        self, name: str, version: str, info: Dict, release: Dict
    ) -> PythonPackage:
        """Creates a PythonPackage matching given name and version."""
        result = None
        logging.getLogger(__name__).debug(
            f"Waiting for GitRepoFound({name}, {version}) events"
        )
        await self._emit_git_repo_requested(name, version, info, release)
        await self._event.wait()
        return self._package

    async def _emit_git_repo_requested(
        self, name: str, version: str, info: Dict, release: Dict
    ):
        self.__class__.register_receiver(self)
        await self.__class__.emit(GitRepoRequested(name, version, info, release))

    async def listenGitRepoFound(self, event: GitRepoFound):
        self.__class__.unregister_receiver(self)
        repo_url, subfolder = GitRepo.extract_url_and_subfolder(event.url)
        git_repo = (
            Ports.instance()
            .resolve(GitRepoRepo)
            .find_by_url_and_rev(repo_url, event.version, subfolder=subfolder)
        )

        if not git_repo:
            logging.getLogger(__name__).warn(
                f"No repository url found for {name}-{version}"
            )
        else:
            for python_package_class in PythonPackage.__subclasses__():
                if python_package_class.git_repo_matches(git_repo):
                    package = python_package_class(
                        name, version, info, release, git_repo
                    )
                    logging.getLogger(__name__).debug(
                        f"Using {python_package_class.__name__} for {git_repo.url}"
                    )
                    break

        if not package:
            raise UnsupportedPythonPackage(name, version)

        self._event.set()

        await self.__class__.emit(PythonPackageCreated(package))

    @classmethod
    def old_create(
        cls, name: str, version: str, info: Dict, release: Dict
    ) -> PythonPackage:
        """Creates a PythonPackage matching given name and version."""
        result = None
        git_repo = PythonPackage.extract_repo(version, info)
        if not git_repo:
            logging.getLogger(__name__).warn(
                f"No repository url found for {name}-{version}"
            )
        else:
            for python_package_class in PythonPackage.__subclasses__():
                if python_package_class.git_repo_matches(git_repo):
                    result = python_package_class(
                        name, version, info, release, git_repo
                    )
                    logging.getLogger(__name__).debug(
                        f"Using {python_package_class.__name__} for {git_repo.url}"
                    )
                    break

        if not result:
            raise UnsupportedPythonPackage(name, version)

        return result


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
