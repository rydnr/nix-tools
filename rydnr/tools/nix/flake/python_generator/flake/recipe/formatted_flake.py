# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/flake/recipe/formatted_flake.py

This file defines the FormattedFlake class.

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
from domain.flake.flake import Flake
from domain.formatting import Formatting
from domain.flake.license import License


class FormattedFlake(Formatting):
    """
    Augments Flake class to include formatting logic required by recipe templates.
    """

    def __init__(self, flk: Flake):
        """Creates a new instance"""
        super().__init__(flk)

    @property
    def flake(self) -> Flake:
        return self._fmt

    def version_with_underscores(self):
        return self.flake.version.replace(".", "_")

    def description(self):
        return self.flake.python_package.info["description"]

    def license(self):
        return License.from_pypi(self.flake.python_package.info.get("license", "")).nix

    def sha256(self):
        return self.flake.python_package.release.get("hash", "")

    def repo_url(self):
        result = ""
        if self.flake.python_package.git_repo:
            result = self.flake.python_package.git_repo.url
        return result

    def repo_rev(self):
        result = ""
        if self.flake.python_package.git_repo:
            result = self.flake.python_package.git_repo.rev
        return result

    def repo_owner(self):
        result = ""
        if self.flake.python_package.git_repo:
            result, _ = self.flake.python_package.git_repo.repo_owner_and_repo_name()
        return result

    def repo_name(self):
        result = ""
        if self.flake.python_package.git_repo:
            _, result = self.flake.python_package.git_repo.repo_owner_and_repo_name()
        return result


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
