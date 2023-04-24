#!/usr/bin/env python3
import sys
from pathlib import Path

base_folder = str(Path(__file__).resolve().parent.parent)
if base_folder not in sys.path:
    sys.path.append(base_folder)

from domain.flake import Flake
from domainport import Port
from domainports import Ports
from domainprimary_port import PrimaryPort
from domaincreate_flake_command import CreateFlake
from domainflake_created_event import FlakeCreated
from domaingithub_git_repo import GithubGitRepo
from domainfolder_flake_repo import FolderFlakeRepo

from typing import Dict, List
import logging
import os
import inspect
import pkgutil
import importlib
import importlib.util
import warnings

for folder in os.scandir("infrastructure"):
    if folder.is_dir():
        sys.path.insert(0, folder.path)

def get_port_interfaces():
    return get_domain_interfaces(Port)

def get_domain_interfaces(iface):
    matches = []
    for _, name, _ in pkgutil.iter_modules(path=["domain"]):
        if name != "this":
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter('ignore', category=DeprecationWarning)
                    module = importlib.import_module(name)
                    for class_name, cls in inspect.getmembers(module, inspect.isclass):
                        if (inspect.getmodule(cls) == module and
                            issubclass(cls, iface) and
                            cls != iface):
                            matches.append(cls)
            except ImportError:
                pass
    return matches


def get_implementations(interface):
    implementations = []
    for _, name, _ in pkgutil.iter_modules(path=sys.path):
        if name != "this":
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter('ignore', category=DeprecationWarning)
                    module = importlib.import_module(name)
                    for class_name, cls in inspect.getmembers(module, inspect.isclass):
                        if (inspect.getmodule(cls) == module and
                            issubclass(cls, interface) and
                            cls != interface):
                            implementations.append(cls)
            except ImportError:
                pass
    return implementations

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

        spec = importlib.util.spec_from_file_location("_log_config", os.path.join("infrastructure", f"_log_config.py"))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        entry = {}
        configure_logging_function = getattr(module, "configure_logging", None)
        if callable(configure_logging_function):
            result.append(configure_logging_function)
        else:
            print(f"Error in infrastructure/_log_config.py: configure_logging")
        return result

    def accept_github_token(self, token: str):
        GithubGitRepo.github_token(token)

    def accept_flakes_folder(self, folder: str):
        FolderFlakeRepo.repo_folder(folder)

    def accept_flakes_url(self, url: str):
        FolderFlakeRepo.flakes_url(url)

if __name__ == "__main__":
    PythonFlakeGenerator.initialize()
    PythonFlakeGenerator.instance().accept_commands()
