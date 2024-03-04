# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/python/build/python_build_resolver.py

This file defines the PythonBuildResolver class.

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
from pythoneda.shared import Event, EventEmitter, EventListener

# from rydnr.tools.nix.flake.python_generator.python.build import PythonBuildStrategyRequested
# from rydnr.tools.nix.flake.python_generator.python import PythonPackage, PythonPackageInProgress
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
        from rydnr.tools.nix.flake.python_generator.python.build import (
            PythonBuildStrategyRequested,
        )

        return [PythonBuildStrategyRequested]

    @classmethod
    async def listenPythonBuildStrategyRequested(
        cls, event  # : PythonBuildStrategyRequested
    ):
        logger = logging.getLogger(__name__)
        package = None
        from rydnr.tools.nix.flake.python_generator.python import (
            PythonPackage,
            PythonPackageInProgress,
        )

        pythonPackageInProgress = PythonPackageInProgress(
            event.package_name, event.package_version, metadata
        )

        for python_package_class in PythonPackage.__subclasses__():
            if python_package_class.git_repo_matches(git_repo):
                package = python_package_class(
                    event.package_name,
                    event.package_version,
                    pythonPackageInProgress.metadata,
                    event.git_repo,
                )
                logging.getLogger(__name__).debug(
                    f"Using {python_package_class.__name__} for {event.git_repo.url}"
                )
                break

        if package:
            self.__class__.emit(package.build_strategy_event())


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
