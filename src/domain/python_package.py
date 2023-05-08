from domain.entity import Entity, attribute, primary_key_attribute
from domain.ports import Ports
from domain.git_repo import GitRepo
from domain.git_repo_repo import GitRepoRepo
from domain.nix_prefetch_url_failed import NixPrefetchUrlFailed
from domain.nix_python_package import NixPythonPackage

import os
import re
import subprocess
import tempfile
from typing import Dict, List

class PythonPackage(Entity):
    """
    Represents a Python package.
    """
    def __init__(self, name: str, version: str, info: Dict, release: Dict, gitRepo: GitRepo):
        """Creates a new PythonPackage instance"""
        super().__init__(id)
        self._name = name
        self._version = version
        self._info = info
        self._release = release
        self._git_repo = gitRepo
        self._nixpkgs_package = None
        self._nixpkgs_found = None
        self._pip_sha256 = None
        self._pip_sha256_failed = None

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

    @classmethod
    def git_repo_matches(cls, gitRepo: GitRepo) -> bool:
        """
        Analyzes given git repository and checks if the subclass is compatible
        """
        raise NotImplementedError("git_repo_matches() must be implemented by subclasses")

    @classmethod
    def fix_url(cls, url: str) -> str:
        result = url
        if result.endswith("/issues"):
            result = result.removesuffix("/issues")
        return result

    @classmethod
    def extract_urls(cls, info: Dict) -> List[str]:
        result = []
        project_urls = info.get("project_urls", {})
        for url in [ entry["collection"].get(entry["key"], None) for entry in [ { "collection": info, "key": "package_url" },{ "collection": info, "key": "home_page" },{ "collection": info, "key": "project_url" },{ "collection": info, "key": "release_url" },{ "collection": project_urls, "key": "Source" },{ "collection": project_urls, "key": "Source Code" },{ "collection": project_urls, "key": "Home" },{ "collection": project_urls, "key": "Homepage" },{ "collection": project_urls, "key": "Changelog" },{ "collection": project_urls, "key": "Documentation" },{ "collection": project_urls, "key": "Issue Tracker" },{ "collection": project_urls, "key": "Tracker" } ] ]:
            if url:
                result.append(cls.fix_url(url))
        return result

    @classmethod
    def extract_repo(cls, version: str, info: Dict) -> GitRepo:
        result = None
        for url in cls.extract_urls(info):
            repo_url, subfolder = GitRepo.extract_url_and_subfolder(url)
            if GitRepo.url_is_a_git_repo(repo_url):
                result = Ports.instance().resolve(GitRepoRepo).find_by_url_and_rev(repo_url, version, subfolder=subfolder)
                break
        return result

    @classmethod
    def extract_dep(cls, depInfo: str) -> tuple:
        pattern = r"([a-zA-Z0-9-_]+)\[?([a-zA-Z0-9-_]+)?\]?([<>=!~]+)?([0-9.]+)?"
        match = re.match(pattern, depInfo)

        name = None
        extras = None
        constraint = None
        version = None
        full_constraint = None

        if match:
            name = match.group(1)
            extras = match.group(2) if match.group(2) else ""
            constraint = match.group(3) if match.group(3) else ""
            version = match.group(4) if match.group(4) else ""

            full_constraint = constraint + version if version else ""

        return name, extras, version, full_constraint

    def find_dep(self, depInfo: str): # -> PythonPackage:
        result = None
        dep_name, _, dep_version, _ = self.__class__.extract_dep(depInfo)
        if dep_name != self.name:
            if dep_version:
                result = Ports.instance().resolvePythonPackageRepo().find_by_name_and_version(dep_name, dep_version)
            else:
                result = Ports.instance().resolvePythonPackageRepo().find_by_name(dep_name)

        return result

    def satisfies_spec(self, nixPythonPackage: NixPythonPackage) -> bool:
        # TODO: check if the nixpkgs package satisfies the version spec
        return True

    def in_nixpkgs(self) -> bool:
        """
        Checks if this package is already in nixpkgs.
        """
        if self._nixpkgs_found is None:
            nixPythonPackageRepo = Ports.instance().resolveNixPythonPackageRepo()
            match = nixPythonPackageRepo.find_by_name_and_version(self.name, self.version)
            result = match != None
            if result:
                self._nixpkgs_package = match
                self._nixpkgs_found = True
            else:
                self._nixpkgs_found = False
                existing = nixPythonPackageRepo.find_by_name(self.name)
                if existing and len(existing) > 0:
                    matches = [pkg for pkg in existing if pkg.is_compatible_with(self.version)]
                    if len(matches) > 0:
                        self._nixpkgs_package = matches[0]
                        self._nixpkgs_found = True
                        result = True
        else:
            result = self._nixpkgs_found

        return result

    def nixpkgs_package_name(self):
        result = None
        if self._nixpkgs_found is None:
            self.in_nixpkgs()
            if self._nixpkgs_found:
                result = self._nixpkgs_package.nixpkgs_package_name()
        elif self._nixpkgs_found:
            result = self._nixpkgs_package.nixpkgs_package_name()

        return result

    def flake_url(self):
        return Ports.instance().resolveFlakeRepo().url_for_flake(self.name, self.version)

    def package_in_pypi(self):
        result = False

        try:
            self.pip_sha256()
            result = True
        except NixPrefetchUrlFailed:
            result = False

        return result

    def pip_sha256(self) -> str:
        result = None
        if self._pip_sha256_failed is None:
            with tempfile.TemporaryDirectory() as temp_dir:
                try:
                    output = subprocess.run(['nix-prefetch-url', f'https://files.pythonhosted.org/packages/source/{self.name[0]}/{self.name}/{self.name}-{self.version}.tar.gz'], check=True, capture_output=True, text=True, cwd=temp_dir)
                    result = output.stdout.splitlines()[-1]
                    self._pip_sha256 = result
                    self._pip_sha256_failed = False
                except subprocess.CalledProcessError:
                    self._pip_sha256_failed = True
                    raise NixPrefetchUrlFailed(self)
        elif self._pip_sha256_failed:
            raise NixPrefetchUrlFailed(self)
        else:
            result = self._pip_sha256

        return result

    def get_native_build_inputs(self) -> List:
        """
        Retrieves the native build inputs.
        """
        raise NotImplementedError('get_native_build_inputs() must be implemented by subclasses')

    def get_propagated_build_inputs(self) -> List:
        """
        Retrieves the propagated build inputs.
        """
        raise NotImplementedError('get_propagated_build_inputs() must be implemented by subclasses')

    def get_build_inputs(self) -> List:
        """
        Retrieves the build inputs.
        """
        raise NotImplementedError('get_build_inputs() must be implemented by subclasses')

    def get_optional_build_inputs(self) -> List:
        """
        Retrieves the optional build inputs.
        """
        raise NotImplementedError('get_optional_build_inputs() must be implemented by subclasses')

    def get_check_inputs(self) -> List:
        """
        Retrieves the check inputs.
        """
        raise NotImplementedError('get_check_inputs() must be implemented by subclasses')

    def get_type(self) -> str:
        """
        Retrieves the type.
        """
        raise NotImplementedError('get_type() must be implemented by subclasses')

    def __str__(self):
        print(f'In PythonPackage.__str__()')
        return super().__str__()

    def _python_package_str(self):
        return super().__str__()

    def _python_package_setattr(self, varName, varValue):
        return super().__setattr__(varName, varValue)

    def _python_package_eq(self, other):
        return super().__eq__(other)

    def _python_package_hash(self):
        return super().__hash__()
