# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/git/git_add_failed.py

This file defines the GitAddFailed class.

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


class GitAddFailed(Exception):
    """
    Adding a file to the git repository failed.
    """

    def __init__(self, file: str, output: str):
        super().__init__(f'"git add {file}" failed')
        self._output = output

    def output(self) -> str:
        return self._output


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
