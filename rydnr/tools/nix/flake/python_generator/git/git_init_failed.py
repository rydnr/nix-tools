class GitInitFailed(Exception):
    """
    git init failed.
    """

    def __init__(self, folder: str, output: str):
        super().__init__(f'"git init" failed (in {folder})')
        self._output = output

    def output(self) -> str:
        return self._output
