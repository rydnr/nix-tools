class GitCheckoutFailed(Exception):
    """
    Running git checkout [rev] failed.
    """

    def __init__(self, url: str, rev: str, folder: str):
        super().__init__('"git checkout {rev}" in folder {folder} failed')
