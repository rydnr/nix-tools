from domain.git.git_repo import GitRepo
from domain.python.python_package_base_event import PythonPackageBaseEvent


class PythonBuildStrategyRequested(PythonPackageBaseEvent):
    """
    Represents the event requesting the build strategy of a Python project.
    """

    def __init__(
        self,
        packageName: str,
        packageVersion: str,
        gitRepo: GitRepo
    ):
        """Creates a new PythonBuildStrategyRequested instance"""
        super().__init__(packageName, packageVersion, gitRepo)
