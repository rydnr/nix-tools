from domain.flake import Flake
from domain.flake_created import FlakeCreated
from domain.flake_recipe import FlakeRecipe
from domain.formatted_flake import FormattedFlake
from domain.license import License
from domain.nix_template import NixTemplate
from domain.ports import Ports
from domain.python_package import PythonPackage
from domain.recipe.formatted_flake_python_package import FormattedFlakePythonPackage
from domain.recipe.formatted_nixpkgs_python_package import FormattedNixpkgsPythonPackage
from domain.recipe.formatted_python_package_list import FormattedPythonPackageList

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
        self._subtemplates = self.extract_dep_templates(flake, list(
                set(flake.python_package.get_native_build_inputs())
            | set(flake.python_package.get_propagated_build_inputs())
            | set(flake.python_package.get_build_inputs())
            | set(flake.python_package.get_check_inputs())
            | set(flake.python_package.get_optional_build_inputs())))

    class Subtemplates(Enum):
        FLAKE_DEPS = "flake_deps"
        NIXPKGS_DEPS = "nixpkgs_deps"
        ALL_DEPS = "all_deps"
        FLAKES_DECLARATION = "flakes_declaration"
        NIXPKGS_DECLARATION = "nixpkgs_declaration"
        FLAKES_AS_PARAMETER_TO_PACKAGE_NIX = "flakes_as_parameter_to_package_nix"
        NIXPKGS_AS_PARAMETER_TO_PACKAGE_NIX = "nixpkgs_as_parameter_to_package_nix"
        DECLARATION = "declaration"
        NIXPKGS_OVERRIDES = "nixpkgs_overrides"

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

    def extract_dep_templates(self, flake, inputs: List[PythonPackage]) -> Dict[str, str]:
        if inputs:
            flake_deps = FormattedPythonPackageList(list([FormattedFlakePythonPackage(dep) for dep in inputs if not dep.in_nixpkgs()]))
            nixpkgs_deps = FormattedPythonPackageList(list([FormattedNixpkgsPythonPackage(dep) for dep in inputs if not dep.in_nixpkgs()]))
            all_deps = FormattedPythonPackageList(flake_deps.list + nixpkgs_deps.list)

            flakes_declaration = FormattedPythonPackageList(flake_deps.list, "flake_declaration")
            nixpkgs_declaration = FormattedPythonPackageList(nixpkgs_deps.list, "nixpkgs_declaration")
            flakes_as_parameter_to_package_nix = FormattedPythonPackageList(flake_deps.list, "as_parameter_to_package_nix")
            nixpkgs_as_parameter_to_package_nix = FormattedPythonPackageList(nixpkgs_deps.list, "as_parameter_to_package_nix")
            declaration = FormattedPythonPackageList(all_deps.list, "name")
            nixpkgs_overrides = FormattedPythonPackageList(nixpkgs_deps.list, "overrides")
        else:
            flake_deps = FormattedPythonPackageList([])
            nixpkgs_deps = FormattedPythonPackageList([])
            all_deps = FormattedPythonPackageList([])
            flakes_declaration = FormattedPythonPackageList([])
            nixpkgs_declaration = FormattedPythonPackageList([])
            flakes_as_parameter_to_package_nix = FormattedPythonPackageList([])
            nixpkgs_as_parameter_to_package_nix = FormattedPythonPackageList([])
            declaration = FormattedPythonPackageList([])
            nixpkgs_overrides = FormattedPythonPackageList([])

        return {
            BaseFlakeRecipe.Subtemplates.FLAKE_DEPS: flake_deps,
            BaseFlakeRecipe.Subtemplates.NIXPKGS_DEPS: nixpkgs_deps,
            BaseFlakeRecipe.Subtemplates.ALL_DEPS: all_deps,
            BaseFlakeRecipe.Subtemplates.FLAKES_DECLARATION: flakes_declaration,
            BaseFlakeRecipe.Subtemplates.NIXPKGS_DECLARATION: nixpkgs_declaration,
            BaseFlakeRecipe.Subtemplates.FLAKES_AS_PARAMETER_TO_PACKAGE_NIX: flakes_as_parameter_to_package_nix,
            BaseFlakeRecipe.Subtemplates.NIXPKGS_AS_PARAMETER_TO_PACKAGE_NIX: nixpkgs_as_parameter_to_package_nix,
            BaseFlakeRecipe.Subtemplates.DECLARATION: declaration,
            BaseFlakeRecipe.Subtemplates.NIXPKGS_OVERRIDES: nixpkgs_overrides
            }

    @property
    def flake(self) -> FormattedFlake:
        return FormattedFlake(self._flake)

    def repo_sha256(self) -> str:
        result = ""
        if self.usesGitrepoSha256():
            result = self._flake.python_package.git_repo.sha256()
        return result

    def pypi_sha256(self) -> str:
        result = ""
        if self.usesPipSha256():
            result = self._flake.python_package.pip_sha256()
        return result

    def native_build_inputs_flakes_declaration(self) -> FormattedPythonPackageList:
        return self._native_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKES_DECLARATION, [])

    def native_build_inputs_nixpkgs_declaration(self) -> FormattedPythonPackageList:
        return self._native_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_DECLARATION, [])

    def native_build_inputs_flake_deps(self) -> FormattedPythonPackageList:
        return self._native_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKE_DEPS, [])

    def native_build_inputs_nixpkgs_deps(self) -> FormattedPythonPackageList:
        return self._native_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_DEPS, [])

    def native_build_inputs_flakes_as_parameter_to_package_nix(self) -> FormattedPythonPackageList:
        return self._native_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKES_AS_PARAMETER_TO_PACKAGE_NIX, [])

    def native_build_inputs_nixpkgs_as_parameter_to_package_nix(self) -> FormattedPythonPackageList:
        return self._native_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_AS_PARAMETER_TO_PACKAGE_NIX, [])

    def native_build_inputs_declaration(self) -> FormattedPythonPackageList:
        return self._native_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.DECLARATION, [])

    def native_build_inputs_nixpkgs_overrides(self) -> FormattedPythonPackageList:
        return self._native_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_OVERRIDES, [])

    def propagated_build_inputs_flakes_declaration(self) -> FormattedPythonPackageList:
        return self._propagated_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKES_DECLARATION, [])

    def propagated_build_inputs_nixpkgs_declaration(self) -> FormattedPythonPackageList:
        return self._propagated_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_DECLARATION, [])

    def propagated_build_inputs_flake_deps(self) -> FormattedPythonPackageList:
        return self._propagated_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKE_DEPS, [])

    def propagated_build_inputs_nixpkgs_deps(self) -> FormattedPythonPackageList:
        return self._propagated_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_DEPS, [])

    def propagated_build_inputs_flakes_as_parameter_to_package_nix(self) -> FormattedPythonPackageList:
        return self._propagated_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKES_AS_PARAMETER_TO_PACKAGE_NIX, [])

    def propagated_build_inputs_nixpkgs_as_parameter_to_package_nix(self) -> FormattedPythonPackageList:
        return self._propagated_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_AS_PARAMETER_TO_PACKAGE_NIX, [])

    def propagated_build_inputs_declaration(self) -> FormattedPythonPackageList:
        return self._propagated_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.DECLARATION, [])

    def propagated_build_inputs_nixpkgs_overrides(self) -> FormattedPythonPackageList:
        return self._propagated_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_OVERRIDES, [])

    def build_inputs_flakes_declaration(self) -> FormattedPythonPackageList:
        return self._build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKES_DECLARATION, [])

    def build_inputs_nixpkgs_declaration(self) -> FormattedPythonPackageList:
        return self._build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_DECLARATION, [])

    def build_inputs_flake_deps(self) -> FormattedPythonPackageList:
        return self._build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKE_DEPS, [])

    def build_inputs_nixpkgs_deps(self) -> FormattedPythonPackageList:
        return self._build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_DEPS, [])

    def build_inputs_flakes_as_parameter_to_package_nix(self) -> FormattedPythonPackageList:
        return self._build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKES_AS_PARAMETER_TO_PACKAGE_NIX, [])

    def build_inputs_nixpkgs_as_parameter_to_package_nix(self) -> FormattedPythonPackageList:
        return self._build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_AS_PARAMETER_TO_PACKAGE_NIX, [])

    def build_inputs_declaration(self) -> FormattedPythonPackageList:
        return self._build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.DECLARATION, [])

    def build_inputs_nixpkgs_overrides(self) -> FormattedPythonPackageList:
        return self._build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_OVERRIDES, [])

    def check_inputs_flakes_declaration(self) -> FormattedPythonPackageList:
        return self._check_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKES_DECLARATION, [])

    def check_inputs_nixpkgs_declaration(self) -> FormattedPythonPackageList:
        return self._check_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_DECLARATION, [])

    def check_inputs_flake_deps(self) -> FormattedPythonPackageList:
        return self._check_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKE_DEPS, [])

    def check_inputs_nixpkgs_deps(self) -> FormattedPythonPackageList:
        return self._check_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_DEPS, [])

    def check_inputs_flakes_as_parameter_to_package_nix(self) -> FormattedPythonPackageList:
        return self._check_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKES_AS_PARAMETER_TO_PACKAGE_NIX, [])

    def check_inputs_nixpkgs_as_parameter_to_package_nix(self) -> FormattedPythonPackageList:
        return self._check_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_AS_PARAMETER_TO_PACKAGE_NIX, [])

    def check_inputs_declaration(self) -> FormattedPythonPackageList:
        return self._check_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.DECLARATION, [])

    def check_inputs_nixpkgs_overrides(self) -> FormattedPythonPackageList:
        return self._check_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_OVERRIDES, [])

    def optional_build_inputs_flakes_declaration(self) -> FormattedPythonPackageList:
        return self._optional_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKES_DECLARATION, [])

    def optional_build_inputs_nixpkgs_declaration(self) -> FormattedPythonPackageList:
        return self._optional_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_DECLARATION, [])

    def optional_build_inputs_flake_deps(self) -> FormattedPythonPackageList:
        return self._optional_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKE_DEPS, [])

    def optional_build_inputs_nixpkgs_deps(self) -> FormattedPythonPackageList:
        return self._optional_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_DEPS, [])

    def optional_build_inputs_flakes_as_parameter_to_package_nix(self) -> FormattedPythonPackageList:
        return self._optional_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.FLAKES_AS_PARAMETER_TO_PACKAGE_NIX, [])

    def optional_build_inputs_nixpkgs_as_parameter_to_package_nix(self) -> FormattedPythonPackageList:
        return self._optional_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_AS_PARAMETER_TO_PACKAGE_NIX, [])

    def optional_build_inputs_declaration(self) -> FormattedPythonPackageList:
        return self._optional_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.DECLARATION, [])

    def optional_build_inputs_nixpkgs_overrides(self) -> FormattedPythonPackageList:
        return self._optional_build_inputs_subtemplates.get(BaseFlakeRecipe.Subtemplates.NIXPKGS_OVERRIDES, [])

    def flakes_as_parameter_to_package_nix(self) -> FormattedPythonPackageList:
        return FormattedPythonPackageList(list(
            set(self.native_build_inputs_flakes_as_parameter_to_package_nix().list)
            | set(self.propagated_build_inputs_flakes_as_parameter_to_package_nix().list)
            | set(self.build_inputs_flakes_as_parameter_to_package_nix().list)
            | set(self.check_inputs_flakes_as_parameter_to_package_nix().list)
            | set(self.optional_build_inputs_flakes_as_parameter_to_package_nix().list)))

    def nixpkgs_as_parameter_to_package_nix(self) -> FormattedPythonPackageList:
        return FormattedPythonPackageList(list(
            set(self.native_build_inputs_nixpkgs_as_parameter_to_package_nix().list)
            | set(self.propagated_build_inputs_nixpkgs_as_parameter_to_package_nix().list)
            | set(self.build_inputs_nixpkgs_as_parameter_to_package_nix().list)
            | set(self.check_inputs_nixpkgs_as_parameter_to_package_nix().list)
            | set(self.optional_build_inputs_nixpkgs_as_parameter_to_package_nix().list)))

    def flakes_declaration(self) -> FormattedPythonPackageList:
        return FormattedPythonPackageList(list(
            set(self.native_build_inputs_flakes_declaration().list)
            | set(self.propagated_build_inputs_flakes_declaration().list)
            | set(self.build_inputs_flakes_declaration().list)
            | set(self.check_inputs_flakes_declaration().list)
            | set(self.optional_build_inputs_flakes_declaration().list)))

    def declaration(self) -> FormattedPythonPackageList:
        return FormattedPythonPackageList(list(
            set(self.native_build_inputs_declaration().list)
            | set(self.propagated_build_inputs_declaration().list)
            | set(self.build_inputs_declaration().list)
            | set(self.check_inputs_declaration().list)
            | set(self.optional_build_inputs_declaration().list)))
