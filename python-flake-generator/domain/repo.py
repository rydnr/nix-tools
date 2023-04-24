import sys
from pathlib import Path

base_folder = str(Path(__file__).resolve().parent.parent)
if base_folder not in sys.path:
    sys.path.append(base_folder)

from domain.port import Port

class Repo(Port):
    def __init__(self, entity_class):
        self._entity_class = entity_class

    @property
    def entity_class(self):
        return self._entity_class
