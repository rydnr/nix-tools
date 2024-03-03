# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/git/_log_config.py

This file defines some logging configuration functions.

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
import logging
import sys


def next_higher_level(level):
    levels = [
        logging.CRITICAL,
        logging.ERROR,
        logging.WARNING,
        logging.INFO,
        logging.DEBUG,
    ]
    for i, current_level in enumerate(levels):
        if level == current_level:
            return levels[i - 1] if i > 0 else current_level
    return level


def configure_logging(verbose: bool, trace: bool, quiet: bool):
    level = logging.WARNING
    if quiet:
        level = logging.ERROR
    elif trace:
        level = logging.DEBUG
    elif verbose:
        level = logging.INFO
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(formatter)
    default_logger = logging.getLogger()
    default_logger.setLevel(level)
    default_logger.addHandler(console_handler)

    default_level = default_logger.getEffectiveLevel()

    next_level = next_higher_level(default_level)

    for name in ["urllib3.connectionpool"]:
        logger = logging.getLogger(name)
        logger.setLevel(next_level)


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
