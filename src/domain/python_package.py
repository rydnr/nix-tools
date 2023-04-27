from domain.entity import Entity, attribute, primary_key_attribute
from domain.ports import Ports
from domain.git_repo import GitRepo
from domain.git_repo_repo import GitRepoRepo
from domain.nix_hash_sha256_failed import NixHashSha256Failed
from domain.nix_python_package import NixPythonPackage
from domain.pip_download_failed import PipDownloadFailed

import logging
import os
import re
import subprocess
import toml
import tempfile
from typing import Dict, List

class PythonPackage(Entity):
    """
    Represents a Python package.
    """
    def __init__(self, name: str, version: str, info: Dict, release: Dict):
        """Creates a new PythonPackage instance"""
        super().__init__(id)
        self._name = name
        self._version = version
        self._info = info
        self._release = release
        self._git_repo = self.analyze_repo()

    @property
    @primary_key_attribute
    def name(self) -> str:
        return self._name

    @property
    @primary_key_attribute
    def version(self) -> str:
        return self._version

    @property
    @attribute
    def info(self) -> Dict:
        return self._info

    @property
    @attribute
    def release(self) -> Dict:
        return self._release

    @property
    @attribute
    def git_repo(self) -> Dict:
        return self._git_repo

    def fix_url(self, url: str) -> str:
        result = url
        if result.endswith("/issues"):
            result = result.removesuffix("/issues")
        return result

    def extract_urls(self) -> List[str]:
        result = []
        project_urls = self._info.get("project_urls", {})
        for url in [ entry["collection"].get(entry["key"], None) for entry in [ { "collection": self._info, "key": "package_url" },{ "collection": self._info, "key": "home_page" },{ "collection": self._info, "key": "project_url" },{ "collection": self._info, "key": "release_url" },{ "collection": project_urls, "key": "Changelog" },{ "collection": project_urls, "key": "Documentation" },{ "collection": project_urls, "key": "Issue Tracker" } ] ]:
            if url:
                result.append(self.fix_url(url))
        return result

    def analyze_repo(self) -> GitRepo:
        result = None
        for url in self.extract_urls():
            if GitRepo.url_is_a_git_repo(url):
                result = Ports.instance().resolve(GitRepoRepo).find_by_url_and_rev(url, self.version)
                break

        if not result:
            logging.getLogger(__name__).warn(f'No repo_url found for {self.name}-{self.version}')

        return result

    def _parse_toml(self, contents: str) -> Dict:
        return toml.loads(contents)

    def _read_pyproject_toml(self) -> Dict:
        result = {}
        if self._git_repo:
            pyprojecttoml_contents = self._git_repo.pyproject_toml()

            if pyprojecttoml_contents:
                result = self._parse_toml(pyprojecttoml_contents)
        return result

    def _read_poetry_lock(self) -> Dict:
        result = {}
        if self._git_repo:
            poetrylock_contents = self._git_repo.poetry_lock()

            if poetrylock_contents:
                result = self._parse_toml(poetrylock_contents)
        return result

    def get_package_type(self) -> str:
        result = "setuptools"
        pyproject_toml = self._read_pyproject_toml()

        if pyproject_toml:
            build_system_requires = pyproject_toml.get("build-system", {}).get("requires", [])
            if any(item.startswith("poetry") for item in build_system_requires):
                result = "poetry"
            elif any(item.startswith("flit") for item in build_system_requires):
                result = "flit"
            elif self._git_repo.pipfile():
                result = "pipenv"

        return result

    def get_poetry_deps(self, section: str) -> List:
        result = []
        pyproject_toml = self._read_pyproject_toml()
        if pyproject_toml:
            poetry_lock = self._read_poetry_lock()
            if poetry_lock:
                for dev_dependency in list(pyproject_toml.get("tool", {}).get("poetry", {}).get(section, {}).keys()):
                    for package in poetry_lock["package"]:
                        if package.get("name", "") == dev_dependency:
                            pythonPackage = Ports.instance().resolvePythonPackageRepo().find_by_name_and_version(dev_dependency, package.get("version", ""))
                            if pythonPackage:
                                result.append(pythonPackage)

        return result

    def get_native_build_inputs(self) -> List:
        result = []
        type = self.get_package_type()
        pyproject_toml = self._read_pyproject_toml()
        if (type == "poetry"):
            result = self.get_native_build_inputs_poetry()
        elif pyproject_toml:
            result = self.get_native_build_inputs_pyproject_toml()
        return result

    def get_native_build_inputs_poetry(self) -> List:
        return self.get_poetry_deps("dev-dependencies")

    def extract_requires(self, required_dep) -> tuple:
        pattern = r"([a-zA-Z0-9-_]+)\[?([a-zA-Z0-9-_]+)?\]?([<>=!~]+)?([0-9.]+)?"
        match = re.match(pattern, required_dep)

        if match:
            name = match.group(1)
            extras = match.group(2) if match.group(2) else ""
            constraint = match.group(3) if match.group(3) else ""
            version = match.group(4) if match.group(4) else ""

            full_constraint = constraint + version if version else ""

            return name, extras, version, full_constraint

        return None

    def get_native_build_inputs_pyproject_toml(self) -> List:
        result = []
        pyproject_toml = self._read_pyproject_toml()
        if pyproject_toml:
            for dev_dependency in list(pyproject_toml.get("build-system", {}).get("requires", [])):
                dep_name, _, dep_version, _ = self.extract_requires(dev_dependency)
                pythonPackage = Ports.instance().resolvePythonPackageRepo().find_by_name_and_version(dep_name, dep_version)
                if pythonPackage:
                    result.append(pythonPackage)

        return result

    def get_propagated_build_inputs(self) -> List:
        result = []
        type = self.get_package_type()
        if (type == "poetry"):
            result = self.get_propagated_build_inputs_poetry()
        #TODO: Support the other build types
        return result

    def get_propagated_build_inputs_poetry(self) -> List:
        return self.get_poetry_deps("dependencies")

    def get_optional_build_inputs(self) -> List:
        result = []
        type = self.get_package_type()
        if (type == "poetry"):
            result = self.get_optional_build_inputs_poetry()
        #TODO: Support the other build types
        return result

    def get_optional_build_inputs_poetry(self) -> List:
        return self.get_poetry_deps("extras")

    def get_check_inputs(self) -> List:
        result = []
        type = self.get_package_type()
        if (type == "poetry"):
            result = self.get_check_inputs_poetry()
        #TODO: Support the other build types
        return result

    def get_check_inputs_poetry(self) -> List:
        return self.get_poetry_deps("test")

    def satisfies_spec(self, nixPythonPackage: NixPythonPackage) -> bool:
        # TODO: check if the nixpkgs package satisfies the version spec
        return True

    def in_nixpkgs(self):
        result = False
        for match in Ports.instance().resolveNixPythonPackageRepo().find_by_name(self.name):
            if self.satisfies_spec(match):
                result = True
                break
        return result

    def nixpkgs_package_name(self):
        nixPythonPackage = Ports.instance().resolveNixPythonPackageRepo().find_by_name_and_version(self.name, self.version)
        if nixPythonPackage:
            return nixPythonPackage.nixpkgs_package_name()
        else:
            return None

    def flake_url(self):
        return Ports.instance().resolveFlakeRepo().url_for_flake(self.name, self.version)

    def pip_sha256(self) -> str:
        result = None
        with tempfile.TemporaryDirectory() as temp_dir:
            # Use pip to download the package
            try:
                subprocess.check_output(['pip', 'download', '--no-deps', '--no-binary', ':all:', f'{self.name}=={self.version}'], stderr=subprocess.STDOUT, cwd=temp_dir)
            except subprocess.CalledProcessError:
                raise PipDownloadFailed(self)
            # Use nix-hash to calculate the sha256
            try:
                output = subprocess.run(['nix-hash', '--type', 'sha256', '--base32', f'{self.name}-{self.version}.tar.gz'], check=True, capture_output=True, text=True, cwd=temp_dir)
                result = output.stdout.splitlines()[-1]
            except subprocess.CalledProcessError:
                raise NixHashSha256Failed(self)

            os.remove(os.path.join(temp_dir, f'{self.name}-{self.version}.tar.gz'))

        logging.getLogger(__name__).debug(f'pypi sha256: {result}')

        return result
