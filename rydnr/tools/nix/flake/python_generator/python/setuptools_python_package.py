from domain.ports import Ports
from domain.git.git_repo import GitRepo
from domain.python.build.setupcfg_utils import SetupcfgUtils
from domain.python.python_package import PythonPackage

import logging
from typing import Dict, List

class SetuptoolsPythonPackage(PythonPackage, SetupcfgUtils):
    """
    Represents a setuptools-based Python package.
    """
    def __init__(self, name: str, version: str, info: Dict, release: Dict, gitRepo: GitRepo):
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
            for dep in setup_cfg.get("options", {}).get("setup_requires", "").split('\n'):
                dep_name, _, _, _ = cls.extract_dep(dep)
                if dep_name == 'setuptools':
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
            for dev_dependency in setup_cfg.get("options", {}).get("setup_requires", "").split('\n'):
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
        for dep in setup_cfg.get("options.extras_require", {}).get("test", "").split('\n'):
            pythonPackage = self.find_dep(dep)
            if pythonPackage:
                result.append(pythonPackage)
        return result
