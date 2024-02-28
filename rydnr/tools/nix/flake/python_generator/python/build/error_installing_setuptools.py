class ErrorInstallingSetuptools(Exception):
    """
    Running python -m pip install setuptools in a virtual environment failed
    """

    def __init__(self):
        super().__init__('"python -m pip install setuptools" failed')
