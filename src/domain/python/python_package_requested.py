from domain.git.git_repo import GitRepo
from domain.python.python_package_base_event import PythonPackageBaseEvent


class PythonPackageRequested(PythonPackageBaseEvent):
    """
    Represents the event requesting a Python project.
    """

    def __init__(self, packageName: str, packageVersion: str):
        """Creates a new PythonPackageRequested instance"""
        super().__init__(packageName, packageVersion, None)
