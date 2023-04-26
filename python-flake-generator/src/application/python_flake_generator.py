#!/usr/bin/env python3
import importlib
import importlib.util
import inspect
import logging
import os
from pathlib import Path
import pkgutil
import sys
from typing import Dict, List
import warnings

base_folder = str(Path(__file__).resolve().parent.parent)
if base_folder not in sys.path:
    sys.path.append(base_folder)

import domain
from domain.create_flake_command import CreateFlake
from domain.flake import Flake
from domain.flake_created_event import FlakeCreated
from domain.port import Port
from domain.ports import Ports
from domain.primary_port import PrimaryPort

import infrastructure
from infrastructure.dynamically_discoverable_flake_recipe_repo import DynamicallyDiscoverableFlakeRecipeRepo
from infrastructure.file_nix_template_repo import FileNixTemplateRepo
from infrastructure.folder_flake_repo import FolderFlakeRepo
from infrastructure.github_git_repo import GithubGitRepo

for folder in os.scandir(os.path.join("src", "infrastructure")):
    if folder.is_dir():
        sys.path.insert(0, folder.path)

def get_port_interfaces():
    return get_domain_interfaces(Port)

def iter_submodules(package):
    result = []
    package_path = Path(package.__path__[0])
    for py_file in package_path.glob('**/*.py'):
        if py_file.is_file():
            relative_path = py_file.relative_to(package_path).with_suffix('')
            module_name = f"{package.__name__}.{relative_path.as_posix().replace('/', '.')}"
            if not module_name in (list(sys.modules.keys())):
                spec = importlib.util.spec_from_file_location(module_name, py_file)
                module = importlib.util.module_from_spec(spec)
                importlib.import_module(module.__name__)
            result.append(sys.modules[module_name])
    return result

def get_domain_interfaces(iface):
    matches = []
    for module in iter_submodules(domain):
        try:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', category=DeprecationWarning)
                for class_name, cls in inspect.getmembers(module, inspect.isclass):
                    if (issubclass(cls, iface) and
                        cls != iface):
                        matches.append(cls)
        except ImportError:
            pass
    return matches

def get_implementations(interface):
    implementations = []
    for module in iter_submodules(infrastructure):
        try:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', category=DeprecationWarning)
                for class_name, cls in inspect.getmembers(module, inspect.isclass):
                    if (issubclass(cls, interface) and
                        cls != interface):
                        implementations.append(cls)
        except ImportError:
            pass
    return implementations

def resolve_port_implementations():
    mappings = {}
    for port in get_port_interfaces():
        implementations = get_implementations(port)
        if len(implementations) == 0:
            logging.getLogger(__name__).critical(f'No implementations found for {port}')
        else:
            mappings.update({ port: implementations[0]() })
    return mappings

class PythonFlakeGenerator():

    _singleton = None

    def __init__(self):
        super().__init__()
        self._primaryPorts = []


    def get_primary_ports(self):
        return self._primaryPorts

    @classmethod
    def initialize(cls):
        cls._singleton = PythonFlakeGenerator()
        mappings = {}
        for port in get_port_interfaces():
            implementations = get_implementations(port)
            if len(implementations) == 0:
                logging.getLogger(__name__).critical(f'No implementations found for {port}')
            else:
                mappings.update({ port: implementations[0]() })
        Ports.initialize(mappings)
        cls._singleton._primaryPorts = get_implementations(PrimaryPort)

    @classmethod
    def instance(cls):
        return cls._singleton

    def delegate_priority(primaryPort):
        return primaryPort().priority()

    def accept_commands(self):
        for primaryPort in sorted(self.get_primary_ports(), key=PythonFlakeGenerator.delegate_priority):
            primaryPort().accept(self)

    def accept_create_flake(self, command: CreateFlake) -> FlakeCreated:
        return Flake.create_flake(command)

    def accept_configure_logging(self, logConfig: Dict[str, bool]):
        for module_functions in self.get_log_configs():
            module_functions(logConfig["verbose"], logConfig["trace"], logConfig["quiet"])

    def get_log_configs(self) -> List[Dict]:
        result = []

        spec = importlib.util.spec_from_file_location("_log_config", os.path.join("src", os.path.join("infrastructure", f"_log_config.py")))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        entry = {}
        configure_logging_function = getattr(module, "configure_logging", None)
        if callable(configure_logging_function):
            result.append(configure_logging_function)
        else:
            print(f"Error in src/infrastructure/_log_config.py: configure_logging")
        return result

    def accept_github_token(self, token: str):
        GithubGitRepo.github_token(token)

    def accept_flakes_folder(self, folder: str):
        FolderFlakeRepo.repo_folder(folder)

    def accept_recipes_folder(self, folder: str):
        FileNixTemplateRepo.recipes_folder(folder)
        DynamicallyDiscoverableFlakeRecipeRepo.recipes_folder(folder)
        DynamicallyDiscoverableFlakeRecipeRepo.initialize()

    def accept_flakes_url(self, url: str):
        FolderFlakeRepo.flakes_url(url)

if __name__ == "__main__":
    PythonFlakeGenerator.initialize()
    PythonFlakeGenerator.instance().accept_commands()
