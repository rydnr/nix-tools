class MoreThanOneFlakeInRecipeToml(Exception):
    """
    A recipe.toml includes more than one entry in its [flake] section.
    """

    def __init__(self, message=None, extra_info=None):
        super().__init__(message)
        self.extra_info = extra_info
