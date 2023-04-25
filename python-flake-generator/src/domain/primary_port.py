import sys
from pathlib import Path

base_folder = str(Path(__file__).resolve().parent.parent)
if base_folder not in sys.path:
    sys.path.append(base_folder)

from domain.port import Port

class PrimaryPort(Port):

    def priority(self) -> int:
        """Must be implemented by subclasses"""
        raise NotImplementedError("priority() must be implemented by subclasses")

    def accept(self, app):
        """Must be implemented by subclasses"""
        raise NotImplementedError("accept() must be implemented by subclasses")
