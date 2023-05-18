from domain.git.git_repo import GitRepo
from domain.python.python_package_base_event import PythonPackageBaseEvent


class SetuppyStrategyFound(PythonPackageBaseEvent):
    """
    Represents the event representing the build strategy of a Python project is setup.py-based.
    """

    def __init__(
        self,
        packageName: str,
        packageVersion: str,
        gitRepo: GitRepo
    ):
        """Creates a new SetuppyStrategyFound instance"""
        super().__init__(packageName, packageVersion, gitRepo)
