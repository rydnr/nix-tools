# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/python/__init__.py

This file ensures rydnr.tools.nix.flake.python_generator.python is a namespace.

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

from .python_package_base_event import PythonPackageBaseEvent
from .python_package_metadata import PythonPackageMetadata
from .python_package_metadata_repo import PythonPackageMetadataRepo
from .python_package_requested import PythonPackageRequested
from .python_package_resolved import PythonPackageResolved
from .python_package_resolver import PythonPackageResolver
from .unsupported_python_package import UnsupportedPythonPackage
from .python_package import PythonPackage
from .python_package_in_progress import PythonPackageInProgress
from .python_package_created import PythonPackageCreated
from .flit_python_package import FlitPythonPackage
from .pipenv_python_package import PipenvPythonPackage
from .poetry_python_package import PoetryPythonPackage
from .setuppy_python_package import SetuppyPythonPackage
from .setuptools_python_package import SetuptoolsPythonPackage
from .python_package_factory import PythonPackageFactory

# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
