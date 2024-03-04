# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/python/build/__init__.py

This file ensures rydnr.tools.nix.flake.python_generator.python.build is a namespace.

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
__path__ = __import__("pkgutil").extend_path(__path__, __name__)

from .error_creating_a_virtual_environment import ErrorCreatingAVirtualEnvironment
from .error_installing_setuptools import ErrorInstallingSetuptools
from .more_than_one_egg_info_folder import MoreThanOneEggInfoFolder
from .no_egg_info_folder_found import NoEggInfoFolderFound
from .pyprojecttoml_utils import PyprojecttomlUtils
from .python_build_resolver import PythonBuildResolver
from .python_build_strategy_requested import PythonBuildStrategyRequested
from .python_setuppy_egg_info_failed import PythonSetuppyEggInfoFailed
from .requirementstxt_utils import RequirementstxtUtils
from .setupcfg_utils import SetupcfgUtils
from .setuppy_strategy_found import SetuppyStrategyFound

# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
