class RecipeDoesNotSupportPlaceholder(Exception):
    """
    A recipe does not include a required placeholder.
    """

    def __init__(self, placeholder: str, functionName: str, recipeClass: str):
        super().__init__(f'Function {functionName} not implemented for placeholder {placeholder} in recipe class {recipeClass}')
