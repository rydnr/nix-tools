# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/git/git_repo_found.py

This file defines the GitRepoFound class.

Copyright (C) 2023-today rydnr's rydnr/python-nix-flake-generator

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from pythoneda.shared import attribute, Event, primary_key_attribute

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
        subfolder: str,
    ):
        """Creates a new GitRepoFound instance"""
        super().__init__()
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


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
