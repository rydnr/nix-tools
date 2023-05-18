class ErrorCreatingAVirtualEnvironment(Exception):
    """
    Running python -m venv [folder] failed
    """

    def __init__(self):
        super().__init__('"python -m venv [folder]" failed')
