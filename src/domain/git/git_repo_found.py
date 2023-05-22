from domain.value_object import attribute, primary_key_attribute
from domain.event import Event

from typing import Dict

class GitRepoFound(Event):
    """
    Represents the event when a git repository has been found for a given Python package.
    """

    def __init__(
        self,
        packageName: str,
        packageVersion: str,
        url: str,
        tag: str,
        metadata: Dict,
        subfolder: str
    ):
        """Creates a new GitRepoFound instance"""
        self._package_name = packageName
        self._package_version = packageVersion
        self._url = url
        self._tag = tag
        self._metadata = metadata
        self._subfolder = subfolder

    @property
    @primary_key_attribute
    def package_name(self):
        return self._package_name

    @property
    @primary_key_attribute
    def package_version(self):
        return self._package_version

    @property
    @primary_key_attribute
    def url(self):
        return self._url

    @property
    @primary_key_attribute
    def tag(self):
        return self._tag

    @property
    @attribute
    def metadata(self):
        return self._metadata

    @property
    @attribute
    def subfolder(self):
        return self._subfolder
