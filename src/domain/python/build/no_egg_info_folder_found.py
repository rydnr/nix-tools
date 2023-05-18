class NoEggInfoFolderFound(Exception):
    """
    There's no .egg-info folder after running 'python setup.py egg_info'.
    """

    def __init__(self):
        super().__init__(
            f'There is no .egg-info folder after running "python setup.py egg_info".'
        )
