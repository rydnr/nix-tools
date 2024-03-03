# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/python/build/requirementstxt_utils.py

This file defines the RequirementstxtUtils class.

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
from typing import List


class RequirementstxtUtils:
    """
    Utilities for dealing with requirements.txt or dev_requirements.txt files
    """

    @classmethod
    def read_requirements_txt(cls, gitRepo) -> List:
        return cls._read_requirements_txt("requirements.txt", gitRepo)

    @classmethod
    def read_dev_requirements_txt(cls, gitRepo) -> List:
        return cls._read_requirements_txt("dev_requirements.txt", gitRepo)

    @classmethod
    def _read_requirements_txt(cls, fileName: str, gitRepo) -> List:
        result = {}
        if gitRepo:
            contents = gitRepo.get_file(fileName)
            if contents:
                result = cls.parse_requirements_txt(contents)
        return result

    @classmethod
    def parse_requirements_txt(cls, contents: str) -> List:
        lines = contents.splitlines()
        # Filter out comments and blank lines
        packages = [
            line.strip()
            for line in lines
            if line.strip() and not line.startswith("#") and not line.startswith("-e ")
        ]
        return packages


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
