from domain.entity import Entity, primary_key_attribute, attribute
from domain.recipe.recipe_does_not_support_placeholder import RecipeDoesNotSupportPlaceholder

import logging
import string

class NixTemplate(Entity):

    """
    Represents a nix template.
    """

    def __init__(self, folder: str, path: str, contents: str):
        """Creates a new nix template instance"""
        super().__init__()
        self._folder = folder
        self._path = path
        self._contents = contents

    @property
    @primary_key_attribute
    def folder(self) -> str:
        return self._folder

    @property
    @primary_key_attribute
    def path(self) -> str:
        return self._path

    @property
    @attribute
    def contents(self) -> str:
        return self._contents

    def render(self, flake, recipe) -> str:

        logging.getLogger(__name__).debug(f'Generating the content of {self.path}')

        newline = '\n'
        tab = '\t'

        return eval(f"""f'''{self._contents}'''""")
