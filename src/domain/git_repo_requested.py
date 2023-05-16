from domain.event import Event

from typing import Dict

class GitRepoRequested(Event):
    """
    Represents the event when a git repository has been requested for a given Python package.
    """

    def __init__(self, packageName: str, packageVersion: str, info: Dict, release: Dict):
        """Creates a new GitRepoRequested instance"""
        self._package_name = packageName
        self._package_version = packageVersion
        self._info = info
        self._release = release

    @property
    def package_name(self):
        return self._package_name

    @property
    def package_version(self):
        return self._package_version

    @property
    def info(self):
        return self._info

    @property
    def release(self):
        return self._release

    def __str__(self):
        return f'{{ "name": "{__name__}", "package_name": "{self.package_name}", "package_version": "{self.package_version}", "info": "{self.info}", "release": "{self.release}" }}'
