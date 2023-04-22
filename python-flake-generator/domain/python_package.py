from entity import Entity, attribute, primary_key_attribute
from ports import Ports
from git_repo import GitRepo
from git_repo_repo import GitRepoRepo

from typing import Dict, List
import toml

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

    def analyze_repo(self) -> GitRepo:
        result = None
        repo_url = self._info["home_page"]
        if GitRepo.url_is_a_git_repo(repo_url):
            result = Ports.instance().resolve(GitRepoRepo).find_by_url_and_rev(repo_url, self._info["version"])
        return result

    def _parse_toml(self, contents: str):
        return toml.loads(contents)

    def _read_pyproject_toml(self):
        pyprojecttoml_contents = self._git_repo.pyproject_toml()

        if pyprojecttoml_contents:
            return self._parse_toml(pyprojecttoml_contents)
        else:
            return None

    def _read_poetry_lock(self):
        poetrylock_contents = self._git_repo.poetry_lock()

        if poetrylock_contents:
            return self._parse_toml(poetrylock_contents)
        else:
            return None

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
        if (type == "poetry"):
            result = self.get_native_build_inputs_poetry()
        #TODO: Support the other build types
        return result

    def get_native_build_inputs_poetry(self) -> List:
        return self.get_poetry_deps("dev-dependencies")

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
