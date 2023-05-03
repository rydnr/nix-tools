#!/usr/bin/env python3

from application.bootstrap import get_interfaces, get_implementations

import importlib
import importlib.util
import logging
import os
from typing import Dict, List

class PythonNixFlakeGenerator():

    _singleton = None

    def __init__(self):
        super().__init__()
        self._primaryPorts = []

    def get_primary_ports(self):
        return self._primaryPorts

    @classmethod
    def initialize(cls):
        cls._singleton = PythonNixFlakeGenerator()
        mappings = {}
        for port in cls.get_port_interfaces():
            # this is to pass the infrastructure module, so I can get rid of the `import infrastructure`
            infrastructureModule = importlib.import_module('.'.join(FileNixTemplateRepo.__module__.split('.')[:-1]))
            implementations = get_implementations(port, infrastructureModule)
            if len(implementations) == 0:
                logging.getLogger(__name__).critical(f'No implementations found for {port}')
            else:
                mappings.update({ port: implementations[0]() })
        Ports.initialize(mappings)
        cls._singleton._primaryPorts = get_implementations(PrimaryPort, infrastructureModule)
        EventListener.find_listeners()
        EventEmitter.register_receiver(cls._singleton)

    @classmethod
    def get_port_interfaces(cls):
        # this is to pass the domain module, so I can get rid of the `import domain`
        return get_interfaces(Port, importlib.import_module('.'.join(Event.__module__.split('.')[:-1])))

    @classmethod
    def instance(cls):
        return cls._singleton

    @classmethod
    def delegate_priority(cls, primaryPort) -> int:
        return primaryPort().priority()

    def accept_input(self):
        for primaryPort in sorted(self.get_primary_ports(), key=PythonNixFlakeGenerator.delegate_priority):
            primaryPort().accept(self)

    def accept_event(self, event): # : Event) -> Event:
        result = []
        if event:
            firstEvents = []
            logging.getLogger(__name__).info(f'Accepting event {event}')
            for listenerClass in EventListener.listeners_for(event.__class__):
                resultingEvents = listenerClass.accept(listenerClass, event)
                if resultingEvents and len(resultingEvents) > 0:
                    firstEvents.extend(resultingEvents)
            if len(firstEvents) > 0:
                result.extend(firstEvents)
                for event in firstEvents:
                    result.extend(self.accept_event(event))
        return result

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

    def accept_forensic_folder(self, folder: str):
        FlakeBuilder.forensic_folder(folder)

    def accept_flakes_url(self, url: str):
        FolderFlakeRepo.flakes_url(url)

if __name__ == "__main__":

    from domain.event import Event
    from domain.event_emitter import EventEmitter
    from domain.event_listener import EventListener
    from domain.flake import Flake
    from domain.flake_builder import FlakeBuilder
    from domain.flake_built import FlakeBuilt
    from domain.flake_created import FlakeCreated
    from domain.port import Port
    from domain.ports import Ports
    from domain.primary_port import PrimaryPort

    from infrastructure.dynamically_discoverable_flake_recipe_repo import DynamicallyDiscoverableFlakeRecipeRepo
    from infrastructure.file_nix_template_repo import FileNixTemplateRepo
    from infrastructure.folder_flake_repo import FolderFlakeRepo
    from infrastructure.github_git_repo import GithubGitRepo

    PythonNixFlakeGenerator.initialize()
    PythonNixFlakeGenerator.instance().accept_input()
