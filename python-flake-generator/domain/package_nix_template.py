import sys
from pathlib import Path

base_folder = str(Path(__file__).resolve().parent.parent)
if base_folder not in sys.path:
    sys.path.append(base_folder)

from domain.nix_template import NixTemplate

from typing import Dict, List

class PackageNixTemplate(NixTemplate):

    """
    Represents a package.nix template.
    """

    def __init__(self, folder: str, path: str, contents: str):
        """Creates a new package.nix template instance"""
        super().__init__(folder, path, contents)
