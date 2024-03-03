# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/python/build/setupcfg_utils.py

This file defines the SetupcfgUtils class.

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
import configparser
from typing import Dict, List


class SetupcfgUtils:
    """
    Utilities for dealing with setup.cfg files
    """

    @classmethod
    def parse_setup_cfg(cls, contents: str) -> Dict:
        config = configparser.ConfigParser()
        config.read_string(contents)
        # Convert to a dictionary
        return {section: dict(config[section]) for section in config.sections()}

    @classmethod
    def read_setup_cfg(cls, gitRepo) -> Dict:
        result = {}
        if gitRepo:
            setupcfg_contents = gitRepo.get_file("setup.cfg")
            if setupcfg_contents:
                result = cls.parse_setup_cfg(setupcfg_contents)
        return result


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
