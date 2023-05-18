class MissingFlakeVersionSpecInRecipeToml(Exception):
    """
    In the recipe.toml, the flake in the [flake] section does not include the version spec.
    """

    def __init__(self, message=None, extra_info=None):
        super().__init__(message)
        self.extra_info = extra_info
