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
from pythoneda.shared.application import enable, PythonEDA
from rydnr.tools.nix.flake.python_generator.infrastructure.cli import (
    BuildFlakeCli,
    CreateFlakeCli,
    FlakesFolderCli,
    FlakesUrlCli,
    ForensicFolderCli,
    GithubTokenCli,
    PackageNameCli,
    PackageVersionCli,
    RecipesFolderCli,
)


@enable(PackageNameCli)
@enable(PackageVersionCli)
@enable(BuildFlakeCli)
@enable(CreateFlakeCli)
@enable(FlakesFolderCli)
@enable(FlakesUrlCli)
@enable(ForensicFolderCli)
@enable(GithubTokenCli)
@enable(RecipesFolderCli)
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
        self._github_token = None
        self._flakes_folder = None
        self._flakes_url = None
        self._recipes_folder = None
        self._forensic_folder = None
        self._package_name = None
        self._package_version = None

    async def accept_github_token(self, token: str):
        """
        Accepts a GitHub token.
        :param token: The GitHub token.
        """
        self._github_token = token

    @property
    def github_token(self):
        """
        Returns the GitHub token.
        :return: The GitHub token.
        """
        return self._github_token

    async def accept_flakes_folder(self, folder: str):
        """
        Accepts the folder where the flakes will be created.
        :param folder: The folder where the flakes will be created.
        """
        self._flakes_folder = folder

    @property
    def flakes_folder(self):
        """
        Returns the folder where the flakes will be created.
        :return: The folder where the flakes will be created.
        """
        return self._flakes_folder

    async def accept_flakes_url(self, url: str):
        """
        Accepts the URL of the flakes.
        :param url: The URL of the flakes.
        """
        self._flakes_url = url

    @property
    def flakes_url(self):
        """
        Returns the URL of the flakes.
        :return: The URL of the flakes.
        """
        return self._flakes_url

    async def accept_recipes_folder(self, folder: str):
        """
        Accepts the folder where the recipes are located.
        :param folder: The folder where the recipes are located.
        """
        self._recipes_folder = folder

    @property
    def recipes_folder(self):
        """
        Returns the folder where the recipes are located.
        :return: The folder where the recipes are located.
        """
        return self._recipes_folder

    async def accept_forensic_folder(self, folder: str):
        """
        Accepts the folder where the forensic information is located.
        :param folder: The folder where the forensic information is located.
        """
        self._forensic_folder = folder

    @property
    def forensic_folder(self):
        """
        Returns the folder where the forensic information is located.
        :return: The folder where the forensic information is located.
        """
        return self._forensic_folder

    async def accept_package_name(self, name: str):
        """
        Accepts the name of the package name.
        :param name: The package name.
        """
        self._package_name = name

    @property
    def package_name(self):
        """
        Returns the name of the package.
        :return: The name of the package.
        """
        return self._package_name

    async def accept_package_version(self, version: str):
        """
        Accepts the package version.
        :param version: The package version.
        """
        self._package_version = version

    @property
    def package_version(self):
        """
        Returns the package version.
        :return: The package version.
        """
        return self._package_version


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
