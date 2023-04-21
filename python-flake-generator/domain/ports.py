from port import Port
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
