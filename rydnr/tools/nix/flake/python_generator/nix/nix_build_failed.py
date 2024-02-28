class NixBuildFailed(Exception):
    """
    nix build failed.
    """

    def __init__(self, folder: str, output: str):
        super().__init__(f'"nix build ." failed (in {folder})')
        self._output = output

    def output(self) -> str:
        return self._output
