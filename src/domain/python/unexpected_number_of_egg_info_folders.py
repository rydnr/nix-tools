class UnexpectedNumberOfEggInfoFolders(Exception):
    """
    Running python setup.py egg_info created an unexpected number of *.egg-info folders.
    """

    def __init__(self):
        super().__init__('"python setup.py egg_info" created more than one .egg-info folder.')
