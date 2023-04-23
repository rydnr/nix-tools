from nix_template import NixTemplate

from typing import Dict

class FlakeNixTemplate(NixTemplate):

    """
    Represents a flake.nix template.
    """

    def __init__(self, folder: str, path: str, contents: str):
        """Creates a new flake.nix template instance"""
        super().__init__(folder, path, contents)
