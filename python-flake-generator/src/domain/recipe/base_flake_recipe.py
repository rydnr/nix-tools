from pathlib import Path
import sys

base_folder = str(Path(__file__).resolve().parent.parent)
if base_folder not in sys.path:
    sys.path.append(base_folder)

from domain.flake import Flake
from domain.flake_created_event import FlakeCreated
from domain.flake_recipe import FlakeRecipe
from domain.nix_template import NixTemplate
from domain.ports import Ports

class BaseFlakeRecipe(FlakeRecipe):

    """
    Represents a base nix flake recipe.
    """

    @classmethod
    def should_initialize(cls) -> bool:
        return cls != BaseFlakeRecipe and super().should_initialize()

    def __init__(self, flake: Flake):
        """Creates a new base nix flake recipe instance"""
        super().__init__(id)
        self._flake = flake

    @classmethod
    def supports(cls, flake: Flake) -> bool:
        "Checks if the recipe class supports given flake"
        return False

    def process(self) -> FlakeCreated:
        result = None
        renderedTemplates = []
        templates = Ports.instance().resolveNixTemplateRepo().find_flake_templates_by_recipe(self)
        if templates:
            for template in [ NixTemplate(t["folder"], t["path"], t["contents"]) for t in templates ]:
                renderedTemplates.append({ "folder": template.folder, "path": template.path, "contents": template.render(self.flake) })
            result = Ports.instance().resolveFlakeRepo().create(self.flake, renderedTemplates)
        return result
