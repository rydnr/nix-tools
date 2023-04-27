class NixHashSha256Failed(Exception):
    """
    Using nix-hash to calculate the sha256 checksum of a pip package failed.
    """
    def __init__(self, message=None, extra_info=None):
        super().__init__(message)
        self.extra_info = extra_info
