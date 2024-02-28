from domain.value_object import attribute, primary_key_attribute
from domain.event import Event
from domain.git.git_repo import GitRepo


class PythonPackageBaseEvent(Event):
    """
    Represents the parent class of PythonPackage events.
    """

    def __init__(
        self,
        packageName: str,
        packageVersion: str,
        gitRepo: GitRepo
    ):
        """Creates a new PythonPackageBaseEvent instance"""
        super().__init__()
        self._package_name = packageName
        self._package_version = packageVersion
        self._git_repo = gitRepo

    @property
    @primary_key_attribute
    def package_name(self):
        return self._package_name

    @property
    @primary_key_attribute
    def package_version(self):
        return self._package_version

    @property
    @attribute
    def git_repo(self):
        return self._git_repo
