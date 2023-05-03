from typing import List

class MoreThanOneEggInfoFolder(Exception):
    """
    There're more than one .egg-info folder after running 'python setup.py egg_info'.
    """

    def __init__(self, folders: List):
        super().__init__(f'There are more than one .egg-info folder after running "python setup.py egg_info": {folders}')
