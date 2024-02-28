from domain.event import Event
from domain.git.git_repo import GitRepo
from domain.ports import Ports
from domain.python.build.error_creating_a_virtual_environment import ErrorCreatingAVirtualEnvironment
from domain.python.build.error_installing_setuptools import ErrorInstallingSetuptools
from domain.python.build.more_than_one_egg_info_folder import MoreThanOneEggInfoFolder
from domain.python.build.no_egg_info_folder_found import NoEggInfoFolderFound
from domain.python.build.python_setuppy_egg_info_failed import PythonSetuppyEggInfoFailed
from domain.python.build.requirementstxt_utils import RequirementstxtUtils
from domain.python.build.setupcfg_utils import SetupcfgUtils
from domain.python.build.setuppy_strategy_found import SetuppyStrategyFound
from domain.python.python_package import PythonPackage

import logging
import os
import subprocess
import sys
import tempfile
from typing import Dict, List

class SetuppyPythonPackage(PythonPackage, SetupcfgUtils, RequirementstxtUtils):
    """
    Represents a setup.py-based Python package.
    """

    def __init__(
        self, name: str, version: str, info: Dict, release: Dict, gitRepo: GitRepo
    ):
        """Creates a new SetuppyPythonPackage instance"""
        super().__init__(name, version, info, release, gitRepo)
        self._requires_txt = None
        self._dev_requirements_txt = None

    @property
    def requires_txt(self) -> Dict:
        if not self._requires_txt:
            self._requires_txt = self.__class__.parse_requires_txt(self.egg_info(self.git_repo))
        return self._requires_txt

    @property
    def dev_requirements_txt(self) -> List:
        if not self._dev_requirements_txt:
            self._dev_requirements_txt = self.__class__.read_dev_requirements_txt(self.git_repo)
        return self._dev_requirements_txt

    @classmethod
    def git_repo_matches(cls, gitRepo: GitRepo) -> bool:
        return gitRepo.get_file("setup.py") is not None or gitRepo.get_file(f'{gitRepo.subfolder}/setup.py') is not None

    def get_type(self) -> str:
        """
        Retrieves the type.
        """
        return "setup.py"

    def append_package(self, packages: List, pythonPackage: PythonPackage, setuptoolsIncluded: bool) -> bool:
        result = False
        if pythonPackage.name != 'setuptools':
            packages.append(pythonPackage)
            result = setuptoolsIncluded
        elif pythonPackage.name == 'setuptools' and not setuptoolsIncluded and self.name != "setuptools":
            packages.append(pythonPackage)
            result = True
        else:
            result = True
        return result

    def get_native_build_inputs(self) -> List:
        result = []
        setuptools_included = False
        sections = self.requires_txt.keys()
        deps = []
        for section in sections:
            if section not in [ "extras_require", "test_require", "test", "dev" ]:
                deps.extend(self.requires_txt[section])
        for dep in deps:
            pythonPackage = self.find_dep(dep)
            if pythonPackage:
                setuptools_included = self.append_package(result, pythonPackage, setuptools_included)
        return result

    def get_propagated_build_inputs(self) -> List:
        return self.get_native_build_inputs()

    def get_build_inputs(self) -> List:
        return self.get_propagated_build_inputs()

    def get_optional_build_inputs(self) -> List:
        result = []
        setuptools_included = False
        extras_require = self.requires_txt.get("extras_require")
        if extras_require:
            for dep in extras_require:
                pythonPackage = self.find_dep(dep)
                if pythonPackage:
                    setuptools_included = self.append_package(result, pythonPackage, setuptools_included)
        dev = self.requires_txt.get("dev")
        if dev:
            for dep in dev:
                pythonPackage = self.find_dep(dep)
                if pythonPackage:
                    setuptools_included = self.append_package(result, pythonPackage, setuptools_included)

        return result

    def get_check_inputs(self) -> List:
        result = []
        setuptools_included = False
        test_require = self.requires_txt.get("test_require")
        if test_require:
            for dep in test_require:
                pythonPackage = self.find_dep(dep)
                if pythonPackage:
                    setuptools_included = self.append_package(result, pythonPackage, setuptools_included)
        test = self.requires_txt.get("test")
        if test:
            for dep in test:
                pythonPackage = self.find_dep(dep)
                if pythonPackage:
                    setuptools_included = self.append_package(result, pythonPackage, setuptools_included)
        for dep in self.dev_requirements_txt:
            pythonPackage = self.find_dep(dep)
            if pythonPackage:
                setuptools_included = self.append_package(result, pythonPackage, setuptools_included)

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
    def python_path(cls, venvFolder: str) -> str:
        if sys.platform == 'win32':
            result = os.path.join(venvFolder, "Scripts", "python.exe")
        else:
            result = os.path.join(venvFolder, "bin", "python")
        return result

    def egg_info(self, gitRepo: GitRepo) -> str:
        result = None

        with tempfile.TemporaryDirectory() as venv_dir:
            self.__class__.create_venv(venv_dir)
            self.__class__.install_setuptools(venv_dir)
            repo_folder = gitRepo.clone(venv_dir, "upstream")
            if gitRepo.subfolder:
                repo_folder = os.path.join(repo_folder, gitRepo.subfolder)
            egg_info_output = self.__class__.run_egg_info(venv_dir, repo_folder)
            result = self.cat_requires_txt(gitRepo, repo_folder, egg_info_output)

        return result

    @classmethod
    def create_venv(cls, folder: str) -> str:
        try:
            output = subprocess.run([sys.executable, '-m', 'venv', folder], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=folder)
        except subprocess.CalledProcessError as err:
            logging.getLogger(__name__).error(err.stdout)
            logging.getLogger(__name__).error(err.stderr)
            raise ErrorCreatingAVirtualEnvironment()

        return output.stdout

    @classmethod
    def install_setuptools(cls, folder: str) -> str:
        try:
            output = subprocess.run([cls.python_path(folder), '-m', 'pip', 'install', 'setuptools'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=folder)
        except subprocess.CalledProcessError as err:
            logging.getLogger(__name__).error(err.stdout)
            logging.getLogger(__name__).error(err.stderr)
            raise ErrorInstallingSetuptools()

        return output.stdout

    @classmethod
    def run_egg_info(cls, venv_folder: str, repo_folder: str) -> str:
        logging.getLogger(__name__).info(f'Running "python setup.py egg_info" from {repo_folder}')
        try:
            output = subprocess.run([cls.python_path(venv_folder), 'setup.py', 'egg_info'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=repo_folder)
        except subprocess.CalledProcessError as err:
            logging.getLogger(__name__).error(err.stdout)
            logging.getLogger(__name__).error(err.stderr)
            raise PythonSetuppyEggInfoFailed()

        return output.stdout

    @classmethod
    def retrieve_package_dir(cls, gitRepo: GitRepo) -> str:
        setup_cfg = cls.read_setup_cfg(gitRepo)
        if setup_cfg:
            result = setup_cfg.get("options", {}).get("package_dir", None)
        else:
            result = None
        return result

    @classmethod
    def normalize(cls, s: str) -> str:
        return ''.join(c if c.isalnum() else '_' for c in s).lower()

    def cat_requires_txt(self, gitRepo: GitRepo, folder: str, eggInfoOutput: str) -> str:
        result = None

        # Retrieve the package dir
        package_dir = self.__class__.retrieve_package_dir(gitRepo)

        if package_dir:
            subfolder = os.path.join(folder, package_dir)
        else:
            subfolder = folder

        # Get the list of all directories in the current directory.
        dirs = os.listdir(subfolder)

        _, name = gitRepo.repo_owner_and_repo_name()
        normalized_name = self.__class__.normalize(name)
        normalized_package_name = self.__class__.normalize(self.name)

        logging.getLogger(__name__).info(f'name: {normalized_name}, package_name: {normalized_package_name}, folder: {folder}, subfolder: {subfolder}, dirs: {dirs}')


        # Filter the list to only include .egg-info directories.
        egg_info_dirs = [d for d in dirs if d.endswith('.egg-info') and (normalized_name in d or normalized_package_name in d)]

        # There should be only one .egg-info directory.
        # If not, you might need to handle this situation.
        if len(egg_info_dirs) == 0:
            logging.getLogger(__name__).error(eggInfoOutput)
            raise NoEggInfoFolderFound()
        if len(egg_info_dirs) == 1:
            egg_info_dir = egg_info_dirs[0]
            with open(os.path.join(subfolder, egg_info_dir, "requires.txt"), "r") as file:
                result = file.read()
        else:
            logging.getLogger(__name__).error(eggInfoOutput)
            raise MoreThanOneEggInfoFolder(egg_info_dirs)

        return result

    def build_strategy_event(self) -> Event:
        """
        Retrieves the associated build strategy event.
        """
        return SetuppyStrategyFound(self)
