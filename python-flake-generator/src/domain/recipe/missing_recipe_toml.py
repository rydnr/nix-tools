class MissingRecipeToml(Exception):
    """
    A recipe does not include its recipe.toml file.
    """
    def __init__(self, message=None, extra_info=None):
        super().__init__(message)
        self.extra_info = extra_info
