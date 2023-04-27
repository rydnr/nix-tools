from domain.flake import Flake
from domain.flake_created_event import FlakeCreated
from domain.flake_recipe import FlakeRecipe
from domain.nix_template import NixTemplate
from domain.ports import Ports

import inspect
import logging
from pathlib import Path
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
        else:
            logging.getLogger(__name__).critical(f'No templates provided by recipe {Path(inspect.getsourcefile(self.__class__)).parent}')
        return result
