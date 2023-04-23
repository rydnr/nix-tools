from entity import Entity, primary_key_attribute, attribute
from python_package import PythonPackage

from typing import Dict, List
import logging
import subprocess
import re

class NixTemplate(Entity):

    """
    Represents a nix template.
    """

    def __init__(self, folder: str, path: str, contents: str):
        """Creates a new nix template instance"""
        super().__init__(id)
        self._folder = folder
        self._path = path
        self._contents = contents

    @property
    @primary_key_attribute
    def folder(self) -> str:
        return self._folder

    @property
    @primary_key_attribute
    def path(self) -> str:
        return self._path

    @property
    @attribute
    def contents(self) -> str:
        return self._contents

    @classmethod
    def get_nix_prefetch_git_hash(cls, url, tag):
        # Use nix-prefetch-git to compute the hash
        result = subprocess.run(['nix-prefetch-git', '--deepClone', f'{url}/tree/{tag}'], check=True, capture_output=True, text=True)
        output = result.stdout

        return output.splitlines()[-1]

    def extract_dep_templates(self, flake, inputs: List[PythonPackage]) -> Dict[str, str]:
        if inputs:
            flakes_declaration = "\n  ".join(f'{dep.name}-flake.url = "{dep.flake_url()}";' for dep in inputs if not dep.in_nixpkgs())
            not_flakes_with_newlines = "\n            ".join(f'{dep.nixpkgs_package_name()} = pkgs.python3Packages.{dep.nixpkgs_package_name()};' for dep in inputs if dep.in_nixpkgs())
            flakes_with_newlines = "\n            ".join(f'{dep.name} = {dep.name}-flake.packages.${{system}}.{dep.name};' for dep in inputs if not flake.dependency_in_nixpkgs(dep))
            with_commas = ", ".join(dep.nixpkgs_package_name() for dep in inputs if dep.in_nixpkgs())
            with_blanks = " ".join(dep.nixpkgs_package_name() for dep in inputs if dep.in_nixpkgs())
            with_newlines = "\n    ".join(dep.nixpkgs_package_name() for dep in inputs if dep.in_nixpkgs())
            declaration = f", {with_commas}"
            overrides = "\n    ".join(f'{dep.nixpkgs_package_name()} = pkgs.python3Packages.{dep.nixpkgs_package_name()};' for dep in inputs if dep.in_nixpkgs())
        else:
            flakes_declaration = ""
            not_flakes_with_newlines = ""
            flakes_with_newlines = ""
            with_commas = ""
            with_blanks = ""
            with_newlines = ""
            declaration = ""
            overrides = ""

        return {
            "flakes_declaration": flakes_declaration,
            "not_flakes_with_newlines": not_flakes_with_newlines,
            "flakes_with_newlines": flakes_with_newlines,
            "with_commas": with_commas,
            "with_blanks": with_blanks,
            "with_newlines": with_newlines,
            "declaration": declaration,
            "overrides": overrides
            }

    def render(self, flake) -> str:

        repo_owner = ""
        repo_name = ""
        repo_url = ""
        repo_rev = ""
        repo_hash = ""
        if flake.python_package.git_repo:
            repo_owner, repo_name = flake.python_package.git_repo.repo_owner_and_repo_name()
            repo_url=flake.python_package.git_repo.url,
            repo_rev=flake.python_package.git_repo.rev,
            repo_hash=flake.python_package.git_repo.repo_info.get("hash", ""),
        native_build_inputs = flake.native_build_inputs
        propagated_build_inputs = flake.propagated_build_inputs
        build_inputs = flake.propagated_build_inputs # TODO: find out whether build inputs can be inferred from the Python package

        native_build_inputs_subtemplates = self.extract_dep_templates(flake, native_build_inputs)
        propagated_build_inputs_subtemplates = self.extract_dep_templates(flake, propagated_build_inputs)
        build_inputs_subtemplates = self.extract_dep_templates(flake, build_inputs)

        native_build_inputs_flakes_declaration = native_build_inputs_subtemplates.get("flakes_declaration", "")
        native_build_inputs_with_blanks = native_build_inputs_subtemplates.get("with_blanks", "")
        native_build_inputs_with_newlines = native_build_inputs_subtemplates.get("with_newlines", "")
        native_build_inputs_flakes_with_newlines = native_build_inputs_subtemplates.get("flakes_with_newlines", "")
        native_build_inputs_not_flakes_with_newlines = native_build_inputs_subtemplates.get("not_flakes_with_newlines", "")
        native_build_inputs_declaration = native_build_inputs_subtemplates.get("declaration", "")
        native_build_inputs_overrides = native_build_inputs_subtemplates.get("overrides", "")
        propagated_build_inputs_flakes_declaration = propagated_build_inputs_subtemplates.get("flakes_declaration", "")
        propagated_build_inputs_with_blanks = propagated_build_inputs_subtemplates.get("with_blanks", "")
        propagated_build_inputs_with_newlines = propagated_build_inputs_subtemplates.get("with_newlines", "")
        propagated_build_inputs_flakes_with_newlines = propagated_build_inputs_subtemplates.get("flakes_with_newlines", "")
        propagated_build_inputs_not_flakes_with_newlines = propagated_build_inputs_subtemplates.get("not_flakes_with_newlines", "")
        propagated_build_inputs_declaration = propagated_build_inputs_subtemplates.get("declaration", "")
        propagated_build_inputs_overrides = propagated_build_inputs_subtemplates.get("overrides", "")
        build_inputs_flakes_declaration = build_inputs_subtemplates.get("flakes_declaration", "")
        build_inputs_with_blanks = build_inputs_subtemplates.get("with_blanks", "")
        build_inputs_with_newlines = build_inputs_subtemplates.get("with_newlines", "")
        build_inputs_flakes_with_newlines = build_inputs_subtemplates.get("flakes_with_newlines", "")
        build_inputs_not_flakes_with_newlines = build_inputs_subtemplates.get("not_flakes_with_newlines", "")
        build_inputs_declaration = build_inputs_subtemplates.get("declaration", "")
        build_inputs_overrides = build_inputs_subtemplates.get("overrides", "")

        return self._contents.format(
            package_name=flake.name,
            package_version=flake.version,
            package_version_with_underscores=flake.version.replace(".", "_"),
            package_description=flake.python_package.info["description"],
            package_license=flake.python_package.info.get("license", ""),
            package_pypi_hash=flake.python_package.release.get("hash", ""),
            repo_url=repo_url,
            repo_rev=repo_rev,
            repo_owner=repo_owner,
            repo_name=repo_name,
            repo_hash=repo_hash,
            native_build_inputs_declaration=native_build_inputs_declaration,
            native_build_inputs_flakes_declaration=native_build_inputs_flakes_declaration,
            native_build_inputs_with_blanks=native_build_inputs_with_blanks,
            native_build_inputs_with_newlines=native_build_inputs_with_newlines,
            native_build_inputs_flakes_with_newlines = native_build_inputs_flakes_with_newlines,
            native_build_inputs_not_flakes_with_newlines = native_build_inputs_not_flakes_with_newlines,
            propagated_build_inputs_declaration=propagated_build_inputs_declaration,
            propagated_build_inputs_flakes_declaration=propagated_build_inputs_flakes_declaration,
            propagated_build_inputs_with_blanks=propagated_build_inputs_with_blanks,
            propagated_build_inputs_with_newlines=propagated_build_inputs_with_newlines,
            propagated_build_inputs_flakes_with_newlines = propagated_build_inputs_flakes_with_newlines,
            propagated_build_inputs_not_flakes_with_newlines = propagated_build_inputs_not_flakes_with_newlines,
            build_inputs_declaration=build_inputs_declaration,
            build_inputs_flakes_declaration=build_inputs_flakes_declaration,
            build_inputs_with_blanks=build_inputs_with_blanks,
            build_inputs_with_newlines=build_inputs_with_newlines,
            build_inputs_flakes_with_newlines = build_inputs_flakes_with_newlines,
            build_inputs_not_flakes_with_newlines = build_inputs_not_flakes_with_newlines,
            not_flake_dependencies_with_newlines=f'{native_build_inputs_not_flakes_with_newlines}{propagated_build_inputs_not_flakes_with_newlines}{build_inputs_not_flakes_with_newlines}',
            flake_dependencies_with_newlines=f'{native_build_inputs_flakes_with_newlines}{propagated_build_inputs_flakes_with_newlines}{build_inputs_flakes_with_newlines}',
            flake_dependencies_declaration=f'{native_build_inputs_flakes_declaration}{propagated_build_inputs_flakes_declaration}{build_inputs_flakes_declaration}',
            dependencies_declaration=f'{native_build_inputs_declaration}{propagated_build_inputs_declaration}{build_inputs_declaration}',
            dependencies_overrides=f'{native_build_inputs_overrides}{propagated_build_inputs_overrides}{build_inputs_overrides}')
