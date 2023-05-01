class PythonSetuppyEggInfoFailed(Exception):
    """
    Running python setup.py egg_info failed.
    """

    def __init__(self):
        super().__init__(
            '"python setup.py egg_info" failed'
        )
