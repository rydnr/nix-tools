import sys
from pathlib import Path

base_folder = str(Path(__file__).resolve().parent.parent)
if base_folder not in sys.path:
    sys.path.append(base_folder)

from domain.port import Port

from typing import Dict

import importlib

class Ports():

    _singleton = None

    def __init__(self, mappings):
        self._mappings = mappings

    @classmethod
    def initialize(cls, mappings: Dict[Port, Port]):
        cls._singleton = Ports(mappings)

    @classmethod
    def instance(cls):
        return cls._singleton

    def resolve(self, port: Port) -> Port:
        return self._mappings.get(port, None)

    def resolveByModuleName(self, module_name: str, port_name: str):
        module = importlib.import_module(module_name)
        port = getattr(module, port_name)
        return self.resolve(port)

    def resolvePythonPackageRepo(self):
        return self.resolveByModuleName("python_package_repo", "PythonPackageRepo")

    def resolveFlakeRepo(self):
        return self.resolveByModuleName("flake_repo", "FlakeRepo")

    def resolveFlakeRecipeRepo(self):
        return self.resolveByModuleName("flake_recipe_repo", "FlakeRecipeRepo")

    def resolveNixTemplateRepo(self):
        return self.resolveByModuleName("nix_template_repo", "NixTemplateRepo")

    def resolveNixPythonPackageRepo(self):
        return self.resolveByModuleName("nix_python_package_repo", "NixPythonPackageRepo")

    def resolveGitRepoRepo(self):
        return self.resolveByModuleName("git_repo_repo", "GitRepoRepo")
