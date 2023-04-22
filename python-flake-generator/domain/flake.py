#!/usr/bin/env python3

from entity import Entity, primary_key_attribute, attribute
from create_flake_command import CreateFlake
from flake_created_event import FlakeCreated
from python_package import PythonPackage
from python_package_repo import PythonPackageRepo
from git_repo import GitRepo
from git_repo_repo import GitRepoRepo
from nix_python_package_repo import NixPythonPackageRepo
from ports import Ports
import os
from pathlib import Path
from typing import Dict, List
import logging

class Flake(Entity):

    """
    Represents a nix flake.
    """
    def __init__(self, name: str, version: str, nativeBuildInputs: List, propagatedBuildInputs: List, optionalBuildInputs: List, dependenciesInNixpkgs: List):
        """Creates a new flake instance"""
        super().__init__(id)
        self._name = name
        self._version = version
        self._native_build_inputs = nativeBuildInputs
        self._propagated_build_inputs = propagatedBuildInputs
        self._optional_build_inputs = optionalBuildInputs
        self._dependencies_in_nixpkgs = dependenciesInNixpkgs

    @property
    @primary_key_attribute
    def name(self) -> str:
        return self._name

    @property
    @primary_key_attribute
    def version(self) -> str:
        return self._version

    @property
    @attribute
    def native_build_inputs(self) -> List:
        return self._native_build_inputs

    @property
    @attribute
    def propagated_build_inputs(self) -> List:
        return self._propagated_build_inputs

    @property
    @attribute
    def optional_build_inputs(self) -> List:
        return self._optional_build_inputs

    @property
    @attribute
    def dependencies_in_nixpkgs(self) -> List:
        return self._dependencies_in_nixpkgs

    @classmethod
    def create_flake(cls, command: CreateFlake) -> FlakeCreated:
        result = None
        logger = logging.getLogger(__name__)
        logger.info(f'Received create-flake ({command.packageName}, {command.packageVersion})')
        flakeRepo = Ports.instance().resolveFlakeRepo()
        # 1. check if flake exists already
        existingFlake = flakeRepo.find_by_name_and_version(command.packageName, command.packageVersion)
        if existingFlake:
            logger.info(f'flake ({command.packageName}, {command.packageVersion}) already exists')
        else:
            # 2. obtain pypi info
            pythonPackage = Ports.instance().resolve(PythonPackageRepo).find_by_name_and_version(command.packageName, command.packageVersion)

            nixPythonPackageRepo = Ports.instance().resolve(NixPythonPackageRepo)
            nativeBuildInputs = pythonPackage.get_native_build_inputs()
            propagatedBuildInputs = pythonPackage.get_propagated_build_inputs()
            optionalBuildInputs = pythonPackage.get_optional_build_inputs()
            dependenciesInNixpkgs = []
            for dep in list(set(nativeBuildInputs) | set(propagatedBuildInputs) | set(optionalBuildInputs)):
                depName = dep.name
                depVersion = dep.version
                nixPythonPackages = nixPythonPackageRepo.find_by_name(dep.name)
                if len(nixPythonPackages) > 0:
                    nixPythonPackage = nixPythonPackages[len(nixPythonPackages) - 1]
                    if pythonPackage.satisfies_spec(nixPythonPackage.version):
                        dependenciesInNixpkgs.append(pythonPackage)
                        depName = nixPythonPackage.name
                        depVersion = nixPythonPackage.version
                # check if there's a flake for the dependency
                depFlake = flakeRepo.find_by_name_and_version(depName, depVersion)
                if depFlake:
                    logger.debug(f'Flake found for {depName}-{depVersion}')
                else:
                    flakeCreated = cls.create_flake(CreateFlake(depName, depVersion))
                    logger.info(f'Flake created for {dep.name}-{dep.version} (triggered by {command.packageName, command.packageVersion})')

            # 3. create flake
            flake = Flake(command.packageName, command.packageVersion, nativeBuildInputs, propagatedBuildInputs, optionalBuildInputs, dependenciesInNixpkgs)
            result = flakeRepo.create(flake, flake.flake_nix(), flake.package_nix())
            if result:
                logger.info(f'flake ({command.packageName}, {command.packageVersion}) created')
            else:
                logger.info(f'flake ({command.packageName}, {command.packageVersion}) could not be created')

        return result

    def flake_nix(self) -> str:
        return "sample flake.nix"

    def package_nix(self) -> str:
        return f"sample {self.name}-{self.version}.nix"

###
    def flake_nix_setuptools_template(package_name: str, package_version: str) -> Dict[str, str]:
        return { "contents": read_resource_file(os.path.join("setuptools", "flake.nix.tmpl")),
                 "folder": f"{package_name}-{package_version}",
                 "path": "flake.nix" }

    def flake_nix_poetry_template(package_name: str, package_version: str) -> Dict[str, str]:
        return { "contents": read_resource_file(os.path.join("poetry", "flake.nix.tmpl")),
                 "folder": f"{package_name}-{package_version}",
                 "path": "flake.nix" }

    def resolve_flake_nix_template(package_name: str, package_version: str, package_type: str) -> Dict[str, str]:
        mapping = {
            "poetry": flake_nix_poetry_template,
            "setuptools": flake_nix_setuptools_template
        }

        result = mapping.get(package_type, None)
        if not result:
            result = flake_nix_setuptools_template

        logging.debug(f"{package_type} -> {result} ")
        return result(package_name, package_version)

    def package_nix_setuptools_pypi_template(package_name: str, package_version: str) -> str:
        return { "contents": read_resource_file(os.path.join("setuptools", "pypi", "package.nix.tmpl")),
                 "folder": f"{package_name}-{package_version}",
                 "path": f"{package_name}-{package_version}.nix" }

    def package_nix_setuptools_github_template(package_name: str, package_version: str) -> str:
        return { "contents": read_resource_file(os.path.join("setuptools", "github", "package.nix.tmpl")),
                 "folder": f"{package_name}-{package_version}",
                 "path": f"{package_name}-{package_version}.nix" }

    def package_nix_poetry_template(package_name: str, package_version: str) -> str:
        return { "contents": read_resource_file(os.path.join("poetry", "package.nix.tmpl")),
                 "folder": f"{package_name}-{package_version}",
                 "path": f"{package_name}-{package_version}.nix" }

    def resolve_package_nix_template(package_name: str, package_version: str, package_type: str) -> str:
        mapping = {
            "poetry": package_nix_poetry_template,
            "setuptools": package_nix_setuptools_github_template
        }
        result = mapping.get(package_type, None)
        if not result:
            result = package_nix_setuptools_github_template

        logging.debug(f"{package_type} -> {result} ")
        return result(package_name, package_version)

    def is_flake(dep: Dict[str, str]) -> bool:
        return dep.get("flake_url", "") != ""

    def extract_dep_templates_for_flake_nix(inputs: Dict[str, str]) -> (str, str, str):
        if inputs:
            flakes_declaration = "\n  ".join(f'{dep["name"]}-flake.url = "{dep.get("flake_url", "")}";' for dep in inputs if is_flake(dep))
            not_flakes_with_newlines = "\n            ".join(f'{extract_name_from_nixpkgs_package(dep["name"])} = pkgs.python3Packages.{extract_name_from_nixpkgs_package(dep["name"])};' for dep in inputs)
            flakes_with_newlines = "\n            ".join(f'{dep["name"]} = {dep["name"]}-flake.packages.${{system}}.{dep["name"]};' for dep in inputs if is_flake(dep))
        else:
            flakes_declaration = ""
            not_flakes_with_newlines = ""
            flakes_with_newlines = ""
        return (flakes_declaration, not_flakes_with_newlines, flakes_with_newlines)

    def extract_dep_templates_for_package_nix(inputs: List[Dict[str, str]]) -> (str, str, str):
        if inputs:
            with_commas = ", ".join(extract_name_from_nixpkgs_package(dep["name"]) for dep in inputs)
            with_blanks = " ".join(extract_name_from_nixpkgs_package(dep["name"]) for dep in inputs)
            with_newlines = "\n    ".join(extract_name_from_nixpkgs_package(dep["name"]) for dep in inputs)
            declaration = f", {with_commas}"
            overrides = "\n    ".join(f'{extract_name_from_nixpkgs_package(dep["name"])} = pkgs.python3Packages.{extract_name_from_nixpkgs_package(dep["name"])};' for dep in inputs)
        else:
            with_commas = ""
            with_blanks = ""
            with_newlines = ""
            declaration = ""
            overrides = ""

        return (with_commas, with_blanks, with_newlines, declaration, overrides)

    def create_nix_file(template: Dict[str, str], base_folder: str, pypi_info: Dict[str, str], github_info: Dict[str, str]):

        package_name = pypi_info["name"]
        package_version = pypi_info["version"]
        folder_name = f"{package_name}-{package_version}"
        package_folder = Path(base_folder) / folder_name
        if not os.path.exists(package_folder):
            os.makedirs(package_folder)
        flake_nix_path = f"{package_folder}/flake.nix"
        package_nix_path = f"{package_folder}/{package_name}-{package_version}.nix"

        package_license = pypi_license_to_nix_license(pypi_info["license"])
        package_description = extract_description(pypi_info.get("description", ""), pypi_info.get("description_content_type", ""))
        github_url = pypi_info["github_url"]
        repo_owner, repo_name = extract_owner_and_repo_name(github_url)

        package_metadata = pypi_info.get("metadata", {})
        package_metadata["native_build_inputs"]=[
            {
                "name": "pip"
            },
            {
                "name": "wheel"
            },
            {
                "name": "packaging"
            },
            {
                "name": "jinja2"
            },
            {
                "name": "markupsafe"
            },
            {
                "name": "aiofiles"
            },
            {
                "name": "chalice"
            },
            {
                "name": "dill"
            },
            {
                "name": "flake8"
            },
            {
                "name": "moto"
            },
            {
                "name": "PyGithub"
            },
            {
                "name": "pytest"
            },
            {
                "name": "typing"
            },
            {
                "name": "tomli"
            },
            {
                "name": "requests"
            },
            {
                "name": "sphinx"
            },
            {
                "name": "tox"
            },
            {
                "name": "aiobotocore"
            },
            {
                "name": "cryptography"
            },
            {
                "name": "cffi"
            }
        ]
        native_build_inputs_flakes_declaration, native_build_inputs_not_flakes_with_newlines, native_build_inputs_flakes_with_newlines = extract_dep_templates_for_flake_nix(package_metadata.get("native_build_inputs", []))
        propagated_build_inputs_flakes_declaration, propagated_build_inputs_not_flakes_with_newlines, propagated_build_inputs_flakes_with_newlines = extract_dep_templates_for_flake_nix(package_metadata.get("propagated_build_inputs", []))
        build_inputs_flakes_declaration, build_inputs_not_flakes_with_newlines, build_inputs_flakes_with_newlines = extract_dep_templates_for_flake_nix(package_metadata.get("build_inputs", []))
        native_build_inputs_with_commas, native_build_inputs_with_blanks, native_build_inputs_with_newlines, native_build_inputs_declaration, native_build_inputs_overrides = extract_dep_templates_for_package_nix(package_metadata.get("native_build_inputs", []))
        propagated_build_inputs_with_commas, propagated_build_inputs_with_blanks, propagated_build_inputs_with_newlines, propagated_build_inputs_declaration, propagated_build_inputs_overrides = extract_dep_templates_for_package_nix(package_metadata.get("propagated_build_inputs", []))
        build_inputs_with_commas, build_inputs_with_blanks, build_inputs_with_newlines, build_inputs_declaration, build_inputs_overrides = extract_dep_templates_for_package_nix(package_metadata.get("build_inputs", []))

        overwrite = True

        path = os.path.join(base_folder, template["folder"], template["path"])

        logging.debug(f'path: {path}')
        if overwrite or not os.path.exists(path):
            logging.debug(f'Creating file: {path}')
            with open(path, "w") as f:
                f.write(template["contents"].format(
                    package_name=package_name,
                    package_version=package_version,
                    package_version_with_underscores=package_version.replace(".", "_"),
                    package_description=package_description,
                    package_license=package_license,
                    package_rev=pypi_info["rev"],
                    package_pypi_hash=pypi_info["hash"],
                    package_github_hash=github_info["hash"],
                    github_url=github_url,
                    repo_owner=repo_owner,
                    repo_name=repo_name,
                    native_build_inputs_flakes_declaration=native_build_inputs_flakes_declaration,
                    propagated_build_inputs_flakes_declaration=propagated_build_inputs_flakes_declaration,
                    build_inputs_flakes_declaration=build_inputs_flakes_declaration,
                    native_build_inputs_with_blanks=native_build_inputs_with_blanks,
                    native_build_inputs_with_newlines=native_build_inputs_with_newlines,
                    propagated_build_inputs_with_blanks=propagated_build_inputs_with_blanks,
                    propagated_build_inputs_with_newlines=propagated_build_inputs_with_newlines,
                    build_inputs_with_blanks=build_inputs_with_blanks,
                    build_inputs_with_newlines=build_inputs_with_newlines,
                    not_flake_dependencies_with_newlines=f"{native_build_inputs_not_flakes_with_newlines}{propagated_build_inputs_not_flakes_with_newlines}{build_inputs_not_flakes_with_newlines}",
                    flake_dependencies_with_newlines=f"{native_build_inputs_flakes_with_newlines}{propagated_build_inputs_flakes_with_newlines}{build_inputs_flakes_with_newlines}",
                    flake_dependencies_declaration=f"{native_build_inputs_flakes_declaration}{propagated_build_inputs_flakes_declaration}{build_inputs_flakes_declaration}",
                    dependencies_declaration=f"{native_build_inputs_declaration}{propagated_build_inputs_declaration}{build_inputs_declaration}",
                    dependencies_overrides=f"{native_build_inputs_overrides}{propagated_build_inputs_overrides}{build_inputs_overrides}",
                ))

    def create_flake_nix_file(base_folder: str, package_type, pypi_info: Dict[str, str], github_info: Dict[str, str]):
        create_nix_file(resolve_flake_nix_template(pypi_info["name"], pypi_info["version"], package_type), base_folder, pypi_info, github_info)

    def create_package_nix_file(base_folder: str, package_type, pypi_info: Dict[str, str], github_info: Dict[str, str]):
        create_nix_file(resolve_package_nix_template(pypi_info["name"], pypi_info["version"], package_type), base_folder, pypi_info, github_info)
