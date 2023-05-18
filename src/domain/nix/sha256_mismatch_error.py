class Sha256MismatchError(Exception):
    """
    The sha256 checksum didn't match.
    """

    def __init__(self, expected: str):
        super().__init__(f'"SHA256 checksum failed. The correct one is "{expected}"')
        self._sha256 = expected

    @property
    def sha256(self) -> str:
        return self._sha256
