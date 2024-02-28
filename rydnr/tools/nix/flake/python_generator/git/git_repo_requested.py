from domain.value_object import attribute, primary_key_attribute
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
    @primary_key_attribute
    def package_name(self):
        return self._package_name

    @property
    @primary_key_attribute
    def package_version(self):
        return self._package_version

    @property
    @attribute
    def info(self):
        return self._info

    @property
    @attribute
    def release(self):
        return self._release
