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
        self._package_name = packageName
        self._package_version = packageVersion
        self._git_repo = gitRepo

    @property
    def package_name(self):
        return self._package_name

    @property
    def package_version(self):
        return self._package_version

    @property
    def git_repo(self):
        return self._git_repo

    def __str__(self):
        if self.git_repo:
            return f'{{ "name": "{self.__class__.__name__}", "package_name": "{self.package_name}", "package_version": "{self.package_version}", "git_repo": "{self.git_repo}" }}'
        else:
            return f'{{ "name": "{self.__class__.__name__}", "package_name": "{self.package_name}", "package_version": "{self.package_version}" }}'

    def __repr__(self):
        if self.git_repo:
            return f'{{ "name": "{self.__class__.__name__}", "package_name": "{self.package_name}", "package_version": "{self.package_version}", "git_repo": "{self.git_repo.__repr__()}" }}'
        else:
            return f'{{ "name": "{self.__class__.__name__}", "package_name": "{self.package_name}", "package_version": "{self.package_version}" }}'

    def __eq__(self, other):
        result = False
        if other is not None:
            if isinstance(other, self.__class__):
                result = (self.package_name == other.package_name) and (self.package_version == other.package_version) and (self.git_repo == other.git_repo)

        return result

    def __hash__(self):
        return hash(tuple([self.package_name, self.package_version, self.git_repo]))
