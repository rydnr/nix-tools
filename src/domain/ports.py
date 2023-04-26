from domain.port import Port

import importlib
from typing import Dict

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

    def resolve_by_module_name(self, module_name: str, port_name: str):
        module = importlib.import_module(module_name)
        port = getattr(module, port_name)
        return self.resolve(port)

    def resolvePythonPackageRepo(self):
        return self.resolve_by_module_name("domain.python_package_repo", "PythonPackageRepo")

    def resolveFlakeRepo(self):
        return self.resolve_by_module_name("domain.flake_repo", "FlakeRepo")

    def resolveFlakeRecipeRepo(self):
        return self.resolve_by_module_name("domain.flake_recipe_repo", "FlakeRecipeRepo")

    def resolveNixTemplateRepo(self):
        return self.resolve_by_module_name("domain.nix_template_repo", "NixTemplateRepo")

    def resolveNixPythonPackageRepo(self):
        return self.resolve_by_module_name("domain.nix_python_package_repo", "NixPythonPackageRepo")

    def resolveGitRepoRepo(self):
        return self.resolve_by_module_name("domain.git_repo_repo", "GitRepoRepo")
