class PipDownloadFailed(Exception):
    """
    A pip package could not be downloaded.
    """

    def __init__(self, message=None, extra_info=None):
        super().__init__(message)
        self.extra_info = extra_info
