class GitAddFailed(Exception):
    """
    Adding a file to the git repository failed.
    """

    def __init__(self, file: str, output: str):
        super().__init__(f'"git add {file}" failed')
        self._output = output

    def output(self) -> str:
        return self._output
