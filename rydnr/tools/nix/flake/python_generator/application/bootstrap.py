# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/application/bootstrap.py

This file defines the Bootstrap class.

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
import importlib
import importlib.util
import inspect
import logging
import os
from pathlib import Path
import pkgutil
import sys
from typing import Dict, List
import warnings

base_folder = str(Path(__file__).resolve().parent.parent)
if base_folder not in sys.path:
    sys.path.append(base_folder)


def iter_submodules(package):
    result = []
    package_path = Path(package.__path__[0])
    for py_file in package_path.glob("**/*.py"):
        if py_file.is_file():
            relative_path = py_file.relative_to(package_path).with_suffix("")
            module_name = (
                f"{package.__name__}.{relative_path.as_posix().replace('/', '.')}"
            )
            if not module_name in (list(sys.modules.keys())):
                spec = importlib.util.spec_from_file_location(module_name, py_file)
                module = importlib.util.module_from_spec(spec)
                importlib.import_module(module.__name__)
            result.append(sys.modules[module_name])
    return result


def get_interfaces(iface, package):
    matches = []
    for module in iter_submodules(package):
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=DeprecationWarning)
                for class_name, cls in inspect.getmembers(module, inspect.isclass):
                    if issubclass(cls, iface) and cls != iface:
                        matches.append(cls)
        except ImportError:
            pass
    return matches


def get_implementations(interface):
    implementations = []
    submodules = iter_submodules(infrastructure)
    for module in submodules:
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=DeprecationWarning)
                for class_name, cls in inspect.getmembers(module, inspect.isclass):
                    if issubclass(cls, interface) and cls != interface:
                        implementations.append(cls)
        except ImportError as err:
            print(f"Error importing {module}: {err}")

    return implementations


import infrastructure

# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
