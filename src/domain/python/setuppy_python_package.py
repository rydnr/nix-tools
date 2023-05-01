from domain.git_repo import GitRepo
from domain.ports import Ports
from domain.python.error_creating_a_virtual_environment import ErrorCreatingAVirtualEnvironment
from domain.python.error_installing_setuptools import ErrorInstallingSetuptools
from domain.python.python_setuppy_egg_info_failed import PythonSetuppyEggInfoFailed
from domain.python.setupcfg_utils import SetupcfgUtils
from domain.python.unexpected_number_of_egg_info_folders import UnexpectedNumberOfEggInfoFolders
from domain.python_package import PythonPackage

import logging
import os
import subprocess
import sys
import tempfile
from typing import Dict, List

class SetuppyPythonPackage(PythonPackage, SetupcfgUtils):
    """
    Represents a setup.py-based Python package.
    """

    def __init__(
        self, name: str, version: str, info: Dict, release: Dict, gitRepo: GitRepo
    ):
        """Creates a new SetuppyPythonPackage instance"""
        super().__init__(name, version, info, release, gitRepo)
        self._requires_txt = None

    @property
    def requires_txt(self) -> Dict:
        if not self._requires_txt:
            self._requires_txt = self.__class__.parse_requires_txt(self.__class__.egg_info(self.git_repo))
        return self._requires_txt

    @classmethod
    def git_repo_matches(cls, gitRepo: GitRepo) -> bool:
        return gitRepo.get_file("setup.py") is not None

    def get_type(self) -> str:
        """
        Retrieves the type.
        """
        return "setup.py"

    def get_native_build_inputs(self) -> List:
        result = []
        setuptools_included = False
        install_requires = self.requires_txt.get("install_requires")
        if install_requires:
            for dep in install_requires:
                pythonPackage = self.find_dep(dep)
                if pythonPackage:
                    result.append(pythonPackage)
                    if pythonPackage.name == 'setuptools':
                        setuptools_included = True
        setup_requires = self.requires_txt.get("setup_requires")
        if setup_requires:
            for dep in setup_requires:
                pythonPackage = self.find_dep(dep)
                if pythonPackage:
                    if pythonPackage.name == 'setuptools':
                        if not setuptools_included and self.name != "setuptools":
                            setuptools_included = True
                            result.append(pythonPackage)
                    else:
                        result.append(pythonPackage)
        if not setuptools_included and self.name != "setuptools":
            result.append(Ports.instance().resolvePythonPackageRepo().find_by_name("setuptools"))
        return result

    def get_propagated_build_inputs(self) -> List:
        return self.get_native_build_inputs()

    def get_build_inputs(self) -> List:
        return self.get_propagated_build_inputs()

    def get_optional_build_inputs(self) -> List:
        result = []
        extras_require = self.requires_txt.get("extras_require")
        if extras_require:
            for dep in extras_require:
                pythonPackage = self.find_dep(dep)
                if pythonPackage:
                    result.append(pythonPackage)
        dev = self.requires_txt.get("dev")
        if dev:
            for dep in dev:
                pythonPackage = self.find_dep(dep)
                if pythonPackage:
                    result.append(pythonPackage)

        return result

    def get_check_inputs(self) -> List:
        result = []
        test_require = self.requires_txt.get("test_require")
        if test_require:
            for dep in test_require:
                pythonPackage = self.find_dep(dep)
                if pythonPackage:
                    result.append(pythonPackage)
        test = self.requires_txt.get("test")
        if test:
            for dep in test:
                pythonPackage = self.find_dep(dep)
                if pythonPackage:
                    result.append(pythonPackage)

        return result

    @classmethod
    def parse_requires_txt(cls, contents: str):
        lines = contents.split('\n')

        current_section = 'default'
        sections = {}
        sections[current_section] = []

        for line in lines:
            line = line.strip()
            if not line:  # Skip empty lines
                continue
            elif line.startswith('[') and line.endswith(']'):  # This is a section line
                current_section = line[1:-1]  # Remove brackets to get section name
                sections[current_section] = []
            else:  # This is a dependency line
                sections[current_section].append(line)

        return sections

    @classmethod
    def egg_info(cls, gitRepo: GitRepo) -> str:
        result = None

        with tempfile.TemporaryDirectory() as venv_dir:
            cls.create_venv(venv_dir)
            cls.install_setuptools(venv_dir)
            repo_folder = gitRepo.clone(venv_dir, "upstream")
            cls.run_egg_info(venv_dir, repo_folder)
            result = cls.cat_requires_txt(gitRepo, repo_folder)

        return result

    @classmethod
    def create_venv(cls, folder: str):
        try:
            subprocess.run([sys.executable, '-m', 'venv', folder], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=folder)
        except subprocess.CalledProcessError as err:
            logging.getLogger(__name__).error(err.stdout)
            logging.getLogger(__name__).error(err.stderr)
            raise ErrorCreatingAVirtualEnvironment()

    @classmethod
    def install_setuptools(cls, folder: str):
        try:
            subprocess.run([os.path.join(folder, 'bin', 'python'), '-m', 'pip', 'install', 'setuptools'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=folder)
        except subprocess.CalledProcessError as err:
            logging.getLogger(__name__).error(err.stdout)
            logging.getLogger(__name__).error(err.stderr)
            raise ErrorInstallingSetuptools()

    @classmethod
    def run_egg_info(cls, venv_folder: str, repo_folder: str):
        try:
            output = subprocess.run([os.path.join(venv_folder, 'bin', 'python'), 'setup.py', 'egg_info'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=repo_folder)
        except subprocess.CalledProcessError as err:
            logging.getLogger(__name__).error(err.stdout)
            logging.getLogger(__name__).error(err.stderr)
            raise PythonSetuppyEggInfoFailed()

    @classmethod
    def retrieve_package_dir(cls, gitRepo: GitRepo, folder: str) -> str:
        setup_cfg = cls.read_setup_cfg(gitRepo)
        if setup_cfg:
            result = setup_cfg.get("options", {}).get("package_dir", None)
        return result

    @classmethod
    def cat_requires_txt(cls, gitRepo: GitRepo, folder: str) -> str:
        result = None

        # Retrieve the package dir
        package_dir = cls.retrieve_package_dir(gitRepo, folder)

        if package_dir:
            subfolder = os.path.join(folder, package_dir)
        else:
            subfolder = folder

        # Get the list of all directories in the current directory.
        dirs = os.listdir(subfolder)

        _, name = gitRepo.repo_owner_and_repo_name()

        # Filter the list to only include .egg-info directories.
        egg_info_dirs = [d for d in dirs if d.endswith('.egg-info') and name in d]

        # There should be only one .egg-info directory.
        # If not, you might need to handle this situation.
        if len(egg_info_dirs) == 1:
            egg_info_dir = egg_info_dirs[0]
            with open(os.path.join(subfolder, egg_info_dir, "requires.txt"), "r") as file:
                result = file.read()

        else:
            raise UnexpectedNumberOfEggInfoFolders()

        return result

    def __str__(self):
        return self._python_package_str()

    def __setattr__(self, varName, varValue):
        return self._python_package_setattr(varName, varValue)

    def __eq__(self, other):
        return self._python_package_eq(other)

    def __hash__(self):
        return self._python_package_hash()
