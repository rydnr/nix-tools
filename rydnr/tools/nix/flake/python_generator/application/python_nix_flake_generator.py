# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/flake/python_nix_flake_generator.py

This file can be used to run python-nix-flake-generator artifact.

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
import asyncio
from pythoneda.shared.application import PythonEDA


class PythonNixFlakeGenerator(PythonEDA):
    """
    Runs the Python Nix flake generator.

    Class name: PythonNixFlakeGenerator

    Responsibilities:
        - Runs the generator.

    Collaborators:
        - None
    """

    def __init__(self):
        """
        Creates a new PythonNixFlakeGenerator instance.
        """
        # python_nix_flake_generator_banner is automatically generated.
        try:
            from rydnr.tools.nix.flake.python_generator.application.python_nix_flake_generator_banner import (
                PythonNixFlakeGeneratorBanner,
            )

            banner = PythonNixFlakeGeneratorBanner()
        except ImportError:
            banner = None
        super().__init__(banner, __file__)


if __name__ == "__main__":
    asyncio.run(
        PythonNixFlakeGenerator.main(
            "rydnr.tools.nix.flake.python_generator.application.PythonNixFlakeGenerator"
        )
    )
# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
