class ErrorCloningGitRepository(Exception):
    """
    Running git clone [url] failed.
    """

    def __init__(self, url: str, folder: str):
        super().__init__('"git clone {url}" in folder {folder} failed')
