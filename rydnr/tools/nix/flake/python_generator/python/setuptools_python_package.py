# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/python/setuptools_python_package.py

This file defines the SetuptoolsPythonPackage class.

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
from pythoneda.shared import Ports
from rydnr.tools.nix.flake.python_generator.git.git_repo import GitRepo
from rydnr.tools.nix.flake.python_generator.python.build.setupcfg_utils import (
    SetupcfgUtils,
)
from rydnr.tools.nix.flake.python_generator.python.python_package import PythonPackage

import logging
from typing import Dict, List


class SetuptoolsPythonPackage(PythonPackage, SetupcfgUtils):
    """
    Represents a setuptools-based Python package.
    """

    def __init__(
        self, name: str, version: str, info: Dict, release: Dict, gitRepo: GitRepo
    ):
        """Creates a new SetuptoolsPythonPackage instance"""
        super().__init__(name, version, info, release, gitRepo)

    @classmethod
    def git_repo_matches(cls, gitRepo: GitRepo) -> bool:
        """
        Analyzes given git repository and checks if the subclass is compatible
        """
        result = False
        setup_cfg = cls.read_setup_cfg(gitRepo)
        if setup_cfg:
            for dep in (
                setup_cfg.get("options", {}).get("setup_requires", "").split("\n")
            ):
                dep_name, _, _, _ = cls.extract_dep(dep)
                if dep_name == "setuptools":
                    result = True
                    break

        return result

    def get_type(self) -> str:
        """
        Retrieves the type.
        """
        return "setuptools"

    def get_native_build_inputs(self) -> List:
        result = []
        setup_cfg = self.read_setup_cfg()
        if setup_cfg:
            for dev_dependency in (
                setup_cfg.get("options", {}).get("setup_requires", "").split("\n")
            ):
                pythonPackage = self.find_dep(dev_dependency)
                if pythonPackage:
                    result.append(pythonPackage)

        return result

    def get_propagated_build_inputs(self) -> List:
        return self.get_native_build_inputs()

    def get_build_inputs_setuptools(self) -> List:
        return self.get_native_build_inputs()

    def get_optional_build_inputs_setuptools(self) -> List:
        # TODO: Check if they are declared in setup.cfg
        return []

    def get_check_inputs(self) -> List:
        result = []
        setup_cfg = self.read_setup_cfg()
        for dep in (
            setup_cfg.get("options.extras_require", {}).get("test", "").split("\n")
        ):
            pythonPackage = self.find_dep(dep)
            if pythonPackage:
                result.append(pythonPackage)
        return result


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
