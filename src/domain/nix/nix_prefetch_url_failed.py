class NixPrefetchUrlFailed(Exception):
    """
    Using nix-prefetch-url to calculate the sha256 checksum of a url failed.
    """
    def __init__(self, message=None, extra_info=None):
        super().__init__(message)
        self.extra_info = extra_info
