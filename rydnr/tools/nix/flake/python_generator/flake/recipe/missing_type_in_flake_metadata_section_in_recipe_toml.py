class MissingTypeInFlakeMetadataSectionInRecipeToml(Exception):
    """
    In the recipe.toml, the [flake.metadata] section does not include the "type" entry.
    """

    def __init__(self, message=None, extra_info=None):
        super().__init__(message)
        self.extra_info = extra_info
