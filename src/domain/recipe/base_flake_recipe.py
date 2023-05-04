from domain.flake import Flake
from domain.flake_created import FlakeCreated
from domain.flake_recipe import FlakeRecipe
from domain.license import License
from domain.nix_template import NixTemplate
from domain.ports import Ports
from domain.python_package import PythonPackage

from enum import Enum
import inspect
import logging
from pathlib import Path
from typing import Dict, List

class BaseFlakeRecipe(FlakeRecipe):

    """
    Represents a base nix flake recipe.
    """
    def __init__(self, flake: Flake):
        """Creates a new base nix flake recipe instance"""
        super().__init__(flake)
        self._native_build_inputs_subtemplates = self.extract_dep_templates(flake, flake.python_package.get_native_build_inputs())
        self._propagated_build_inputs_subtemplates = self.extract_dep_templates(flake, flake.python_package.get_propagated_build_inputs())
        self._build_inputs_subtemplates = self.extract_dep_templates(flake, flake.python_package.get_build_inputs())
        self._check_inputs_subtemplates = self.extract_dep_templates(flake, flake.python_package.get_check_inputs())
        self._optional_build_inputs_subtemplates = self.extract_dep_templates(flake, flake.python_package.get_optional_build_inputs())
        self._subtemplates = self.extract_dep_templates(flake, list(set(flake.python_package.get_native_build_inputs()) | set(flake.python_package.get_propagated_build_inputs()) | set(flake.python_package.get_build_inputs()) | set(flake.python_package.get_check_inputs()) | set(flake.python_package.get_optional_build_inputs())))

    class Subtemplates(Enum):
        FLAKES_DECLARATION = "flakes_declaration"
        NOT_FLAKES_DECLARATION = "not_flakes_declaration"
        FLAKES_WITH_NEWLINES = "flakes_with_newlines"
        NOT_FLAKES_WITH_NEWLINES = "not_flakes_with_newlines"
        FLAKES_NAMES_WITH_COMMAS = "flakes_names_with_commas"
        NIXPKGS_NAMES_WITH_COMMAS = "nixpkgs_names_with_commas"
        FLAKES_NAMES_WITH_BLANKS = "flakes_names_with_blanks"
        NIXPKGS_NAMES_WITH_BLANKS = "nixpkgs_names_with_blanks"
        NAMES_WITH_NEWLINES = "names_with_newlines"
        FLAKES_NAMES_WITH_NEWLINES = "flakes_names_with_newlines"
        NIXPKGS_NAMES_WITH_NEWLINES = "nixpkgs_names_with_newlines"
        DECLARATION = "declaration"
        NOT_FLAKES_OVERRIDES = "not_flakes_overrides"

    @classmethod
    def should_initialize(cls) -> bool:
        return cls != BaseFlakeRecipe and super().should_initialize()

    @classmethod
    def supports(cls, flake: Flake) -> bool:
        "Checks if the recipe class supports given flake"
        return False

    def process(self) -> FlakeCreated:
        result = None
        renderedTemplates = []
        templates = Ports.instance().resolveNixTemplateRepo().find_flake_templates_by_recipe(self)
        if templates:
            for template in [ NixTemplate(t["folder"], t["path"], t["contents"]) for t in templates ]:
                renderedTemplates.append({ "folder": template.folder, "path": template.path, "contents": template.render(self.flake, self) })
            result = Ports.instance().resolveFlakeRepo().create(self.flake, renderedTemplates, self)
        else:
            logging.getLogger(__name__).critical(f'No templates provided by recipe {Path(inspect.getsourcefile(self.__class__)).parent}')
        return result

    def package_name_value(self):
        return self.flake.name

    def extract_dep_templates(self, flake, inputs: List[PythonPackage]) -> Dict[str, str]:
        if inputs:
            flakes_declaration = "\n  ".join(f'    {dep.name}-flake.url = "{dep.flake_url()}";' for dep in inputs if dep.in_nixpkgs())
            not_flakes_declaration = "\n            ".join(f'{dep.nixpkgs_package_name()} = pkgs.python3Packages.{dep.nixpkgs_package_name()};' for dep in inputs if not dep.in_nixpkgs())
            flakes_with_newlines = "\n            ".join(f'{dep.name} = {dep.name}-flake.packages.${{system}}.{dep.name};' for dep in inputs if not dep.in_nixpkgs())
            not_flakes_with_newlines = "\n            ".join(dep.nixpkgs_package_name() for dep in inputs if dep.in_nixpkgs())
            flakes_names_with_commas = ", ".join(dep.name for dep in inputs if not dep.in_nixpkgs())
            nixpkgs_names_with_commas = ", ".join(dep.name for dep in inputs if not dep.in_nixpkgs())
            flakes_names_with_blanks = " ".join(dep.name for dep in inputs if dep.in_nixpkgs())
            nixpkgs_names_with_blanks = " ".join(dep.nixpkgs_package_name() for dep in inputs if dep.in_nixpkgs())
            names_with_newlines = "\n    ".join(dep.name for dep in inputs)
            flakes_names_with_newlines = "\n    ".join(dep.name for dep in inputs if not dep.in_nixpkgs())
            nixpkgs_names_with_newlines = "\n    ".join(dep.nixpkgs_package_name() for dep in inputs if dep.in_nixpkgs())
            declaration = ", ".join(dep.name for dep in inputs)
            if declaration != "":
                declaration = f', {declaration}'
            not_flakes_overrides = "\n    ".join(f'{dep.nixpkgs_package_name()} = pkgs.python3Packages.{dep.nixpkgs_package_name()};' for dep in inputs if dep.in_nixpkgs())
        else:
            flakes_declaration = ""
            not_flakes_declaration = ""
            not_flakes_with_newlines = ""
            flakes_with_newlines = ""
            flakes_names_with_commas = ""
            nixpkgs_names_with_commas = ""
            flakes_names_with_blanks = ""
            nixpkgs_names_with_blanks = ""
            flakes_names_with_newlines = ""
            nixpkgs_names_with_newlines = ""
            declaration = ""
            not_flakes_overrides = ""

        return {
            BaseFlakeRecipe.Subtemplates.FLAKES_DECLARATION: flakes_declaration,
            BaseFlakeRecipe.Subtemplates.NOT_FLAKES_DECLARATION: not_flakes_declaration,
            BaseFlakeRecipe.Subtemplates.FLAKES_WITH_NEWLINES: flakes_with_newlines,
            BaseFlakeRecipe.Subtemplates.NOT_FLAKES_WITH_NEWLINES: not_flakes_with_newlines,
            BaseFlakeRecipe.Subtemplates.FLAKES_NAMES_WITH_COMMAS: flakes_names_with_commas,
            BaseFlakeRecipe.Subtemplates.NIXPKGS_NAMES_WITH_COMMAS: nixpkgs_names_with_commas,
            BaseFlakeRecipe.Subtemplates.FLAKES_NAMES_WITH_BLANKS: flakes_names_with_blanks,
            BaseFlakeRecipe.Subtemplates.NIXPKGS_NAMES_WITH_BLANKS: nixpkgs_names_with_blanks,
            BaseFlakeRecipe.Subtemplates.FLAKES_NAMES_WITH_NEWLINES: flakes_names_with_newlines,
            BaseFlakeRecipe.Subtemplates.NIXPKGS_NAMES_WITH_NEWLINES: nixpkgs_names_with_newlines,
            BaseFlakeRecipe.Subtemplates.DECLARATION: declaration,
            BaseFlakeRecipe.Subtemplates.NOT_FLAKES_OVERRIDES: not_flakes_overrides
            }

    def package_version_value(self):
        return self.flake.version

    def package_version_with_underscores_value(self):
        return self.flake.version.replace(".", "_")

    def package_description_value(self):
        return self.flake.python_package.info["description"]

    def package_license_value(self):
        return License.from_pypi(self.flake.python_package.info.get("license", "")).nix

    def package_sha256_value(self):
        return self.flake.python_package.release.get("hash", "")

    def repo_url_value(self):
        result = ""
        if self.flake.python_package.git_repo:
            result = self.flake.python_package.git_repo.url
        return result

    def repo_rev_value(self):
        result = ""
        if self.flake.python_package.git_repo:
            result = self.flake.python_package.git_repo.rev
        return result

    def repo_owner_value(self):
        result = ""
        if self.flake.python_package.git_repo:
            result, _ = self.flake.python_package.git_repo.repo_owner_and_repo_name()
        return result

    def repo_name_value(self):
        result = ""
        if self.flake.python_package.git_repo:
            _, result = self.flake.python_package.git_repo.repo_owner_and_repo_name()
        return result

    def repo_sha256_value(self):
        result = ""
        if self.usesGitrepoSha256():
            result = self.flake.python_package.git_repo.sha256()
        return result

    def pypi_sha256_value(self):
        result = ""
        if self.usesPipSha256():
            result = self.flake.python_package.pip_sha256()
        return result

    def native_build_inputs_declaration_value(self):
        return self._native_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.DECLARATION, "")

    def native_build_inputs_flakes_declaration_value(self):
        return self._native_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKES_DECLARATION, "")

    def native_build_inputs_not_flakes_declaration_value(self):
        return self._native_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NOT_FLAKES_DECLARATION, "")

    def native_build_inputs_flakes_names_with_blanks_value(self):
        return self._native_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKES_NAMES_WITH_BLANKS, "")

    def native_build_inputs_nixpkgs_names_with_blanks_value(self):
        return self._native_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_NAMES_WITH_BLANKS, "")

    def native_build_inputs_flakes_names_with_commas_value(self):
        return self._native_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKES_NAMES_WITH_COMMAS, "")

    def native_build_inputs_nixpkgs_names_with_commas_value(self):
        return self._native_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_NAMES_WITH_COMMAS, "")

    def native_build_inputs_names_with_newlines_value(self):
        return self._native_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NAMES_WITH_NEWLINES, "")

    def native_build_inputs_flakes_names_with_newlines_value(self):
        return self._native_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKES_NAMES_WITH_NEWLINES, "")

    def native_build_inputs_nixpkgs_names_with_newlines_value(self):
        return self._native_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_NAMES_WITH_NEWLINES, "")

    def native_build_inputs_flakes_with_newlines_value(self):
        return self._native_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKES_WITH_NEWLINES, "")

    def native_build_inputs_not_flakes_with_newlines_value(self):
        return self._native_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NOT_FLAKES_WITH_NEWLINES, "")

    def propagated_build_inputs_declaration_value(self):
        return self._propagated_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.DECLARATION, "")

    def propagated_build_inputs_flakes_declaration_value(self):
        return self._propagated_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKES_DECLARATION, "")

    def propagated_build_inputs_not_flakes_declaration_value(self):
        return self._propagated_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NOT_FLAKES_DECLARATION, "")

    def propagated_build_inputs_flakes_names_with_blanks_value(self):
        return self._propagated_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKES_NAMES_WITH_BLANKS, "")

    def propagated_build_inputs_nixpkgs_names_with_blanks_value(self):
        return self._propagated_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_NAMES_WITH_BLANKS, "")

    def propagated_build_inputs_flakes_names_with_commas_value(self):
        return self._propagated_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKES_NAMES_WITH_COMMAS, "")

    def propagated_build_inputs_nixpkgs_names_with_commas_value(self):
        return self._propagated_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_NAMES_WITH_COMMAS, "")

    def propagated_build_inputs_names_with_newlines_value(self):
        return self._propagated_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NAMES_WITH_NEWLINES, "")

    def propagated_build_inputs_nixpkgs_names_with_newlines_value(self):
        return self._propagated_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_NAMES_WITH_NEWLINES, "")

    def propagated_build_inputs_flakes_names_with_newlines_value(self):
        return self._propagated_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKES_NAMES_WITH_NEWLINES, "")

    def propagated_build_inputs_flakes_with_newlines_value(self):
        return self._propagated_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKES_WITH_NEWLINES, "")

    def propagated_build_inputs_not_flakes_with_newlines_value(self):
        return self._propagated_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NOT_FLAKES_WITH_NEWLINES, "")

    def build_inputs_declaration_value(self):
        return self._build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.DECLARATION, "")

    def build_inputs_flakes_declaration_value(self):
        return self._build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKES_DECLARATION, "")

    def build_inputs_not_flakes_declaration_value(self):
        return self._build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NOT_FLAKES_DECLARATION, "")

    def build_inputs_flakes_names_with_blanks_value(self):
        return self._build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKES_NAMES_WITH_BLANKS, "")

    def build_inputs_nixpkgs_names_with_blanks_value(self):
        return self._build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_NAMES_WITH_BLANKS, "")

    def build_inputs_flakes_names_with_commas_value(self):
        return self._build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKES_NAMES_WITH_COMMAS, "")

    def build_inputs_nixpkgs_names_with_commas_value(self):
        return self._build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_NAMES_WITH_COMMAS, "")

    def build_inputs_flakes_names_with_newlines_value(self):
        return self._build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKES_NAMES_WITH_NEWLINES, "")

    def build_inputs_names_with_newlines_value(self):
        return self._build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NAMES_WITH_NEWLINES, "")

    def build_inputs_nixpkgs_names_with_newlines_value(self):
        return self._build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_NAMES_WITH_NEWLINES, "")

    def build_inputs_flakes_with_newlines_value(self):
        return self._build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKES_WITH_NEWLINES, "")

    def build_inputs_not_flakes_with_newlines_value(self):
        return self._build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NOT_FLAKES_WITH_NEWLINES, "")

    def check_inputs_declaration_value(self):
        return self._check_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.DECLARATION, "")

    def check_inputs_flakes_declaration_value(self):
        return self._check_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKES_DECLARATION, "")

    def check_inputs_not_flakes_declaration_value(self):
        return self._check_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NOT_FLAKES_DECLARATION, "")

    def check_inputs_flakes_names_with_blanks_value(self):
        return self._check_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKES_NAMES_WITH_BLANKS, "")

    def check_inputs_nixpkgs_names_with_blanks_value(self):
        return self._check_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_NAMES_WITH_BLANKS, "")

    def check_inputs_flakes_names_with_commas_value(self):
        return self._check_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKES_NAMES_WITH_COMMAS, "")

    def check_inputs_nixpkgs_names_with_commas_value(self):
        return self._check_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_NAMES_WITH_COMMAS, "")

    def check_inputs_flakes_names_with_blanks_value(self):
        return self._check_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKES_NAMES_WITH_BLANKS, "")

    def check_inputs_nixpkgs_names_with_blanks_value(self):
        return self._check_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_NAMES_WITH_BLANKS, "")

    def check_inputs_names_with_newlines_value(self):
        return self._check_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NAMES_WITH_NEWLINES, "")

    def check_inputs_flakes_names_with_newlines_value(self):
        return self._check_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKES_NAMES_WITH_NEWLINES, "")

    def check_inputs_nixpkgs_names_with_newlines_value(self):
        return self._check_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_NAMES_WITH_NEWLINES, "")

    def check_inputs_not_flakes_with_newlines_value(self):
        return self._check_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NOT_FLAKES_WITH_NEWLINES, "")

    def check_inputs_declaration_value(self):
        return self._check_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.DECLARATION, "")

    def optional_inputs_flakes_declaration_value(self):
        return self._optional_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKES_DECLARATION, "")

    def optional_inputs_not_flakes_declaration_value(self):
        return self._optional_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NOT_FLAKES_DECLARATION, "")

    def optional_inputs_flakes_names_with_blanks_value(self):
        return self._optional_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKES_NAMES_WITH_BLANKS, "")

    def optional_inputs_nixpkgs_names_with_blanks_value(self):
        return self._optional_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_NAMES_WITH_BLANKS, "")

    def optional_inputs_flakes_names_with_commas_value(self):
        return self._optional_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKES_NAMES_WITH_COMMAS, "")

    def optional_inputs_nixpkgs_names_with_commas_value(self):
        return self._optional_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_NAMES_WITH_COMMAS, "")

    def optional_inputs_flakes_names_with_blanks_value(self):
        return self._optional_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKES_NAMES_WITH_BLANKS, "")

    def optional_inputs_nixpkgs_names_with_blanks_value(self):
        return self._optional_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_NAMES_WITH_BLANKS, "")

    def optional_inputs_names_with_newlines_value(self):
        return self._optional_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NAMES_WITH_NEWLINES, "")

    def optional_inputs_flakes_names_with_newlines_value(self):
        return self._optional_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKES_NAMES_WITH_NEWLINES, "")

    def optional_inputs_nixpkgs_names_with_newlines_value(self):
        return self._optional_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_NAMES_WITH_NEWLINES, "")

    def optional_inputs_not_flakes_with_newlines_value(self):
        return self._optional_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NOT_FLAKES_WITH_NEWLINES, "")

    def not_flake_dependencies_with_newlines_value(self):
        return self._subtemplates.get(BaseFlakeRecipe.Subtemplates.NOT_FLAKES_WITH_NEWLINES, "")

    def flake_dependencies_with_newlines_value(self):
        return self._subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKES_WITH_NEWLINES, "")

    def flake_dependencies_declaration_value(self):
        return self._subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKES_DECLARATION, "")

    def dependencies_declaration_value(self):
        return self._subtemplates.get(BaseFlakeRecipe.Subtemplates.DECLARATION, "")

    def dependencies_not_flakes_overrides_value(self):
        return self._subtemplates.get(BaseFlakeRecipe.Subtemplates.NOT_FLAKES_OVERRIDES, "")

    def dependencies_with_newlines_value(self):
        return f'{self._subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKES_NAMES_WITH_NEWLINES, "")}{self._subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_NAMES_WITH_NEWLINES, "")}'

    def dependencies_with_blanks_value(self):
        return f'{self._subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKES_NAMES_WITH_BLANKS, "")}{self._subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_NAMES_WITH_BLANKS, "")}'
