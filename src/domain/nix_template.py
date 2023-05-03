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
        super().__init__(id)
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

        parsed_contents = list(string.Formatter().parse(self._contents))

        placeholders = {}

        for placeholder in [field_name for (_, field_name, _, _) in parsed_contents if field_name is not None]:
            function_name = f'{placeholder}_value'
            if hasattr(recipe, function_name):
                placeholders[placeholder] = getattr(recipe, function_name)()
            else:
                raise RecipeDoesNotSupportPlaceholder(placeholder, function_name, recipe.__class__)

        return self._contents.format(**placeholders)
