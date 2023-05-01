from domain.entity import Entity, attribute, primary_key_attribute
from domain.ports import Ports
from domain.git_repo import GitRepo
from domain.git_repo_repo import GitRepoRepo
from domain.nix_prefetch_url_failed import NixPrefetchUrlFailed
from domain.nix_python_package import NixPythonPackage

import configparser
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
    def __init__(self, name: str, version: str, info: Dict, release: Dict, gitRepo: GitRepo):
        """Creates a new PythonPackage instance"""
        super().__init__(id)
        self._name = name
        self._version = version
        self._info = info
        self._release = release
        self._git_repo = gitRepo

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
        for url in [ entry["collection"].get(entry["key"], None) for entry in [ { "collection": info, "key": "package_url" },{ "collection": info, "key": "home_page" },{ "collection": info, "key": "project_url" },{ "collection": info, "key": "release_url" },{ "collection": project_urls, "key": "Changelog" },{ "collection": project_urls, "key": "Documentation" },{ "collection": project_urls, "key": "Issue Tracker" } ] ]:
            if url:
                result.append(cls.fix_url(url))
        return result

    @classmethod
    def extract_repo(cls, version: str, info: Dict) -> GitRepo:
        result = None
        for url in cls.extract_urls(info):
            if GitRepo.url_is_a_git_repo(url):
                result = Ports.instance().resolve(GitRepoRepo).find_by_url_and_rev(url, version)
                break
        return result

    @classmethod
    def extract_requires(cls, dep) -> tuple:
        pattern = r"([a-zA-Z0-9-_]+)\[?([a-zA-Z0-9-_]+)?\]?([<>=!~]+)?([0-9.]+)?"
        match = re.match(pattern, dep)

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
            try:
                output = subprocess.run(['nix-prefetch-url', f'https://files.pythonhosted.org/packages/source/{self.name[0]}/{self.name}/{self.name}-{self.version}.tar.gz'], check=True, capture_output=True, text=True, cwd=temp_dir)
                result = output.stdout.splitlines()[-1]
            except subprocess.CalledProcessError:
                raise NixPrefetchUrlFailed(self)

        logging.getLogger(__name__).debug(f'pypi sha256: {result}')

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
