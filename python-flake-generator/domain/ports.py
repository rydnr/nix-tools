from port import Port
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
