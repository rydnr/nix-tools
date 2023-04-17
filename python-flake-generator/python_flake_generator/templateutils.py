#!/usr/bin/env python3

from descriptionutils import extract_description
from licenseutils import pypi_license_to_nix_license
from resourcesutils import read_resource_file
import os
from pathlib import Path
from typing import Dict, List
import logging

def flake_nix_setuptools_template() -> str:
    return read_resource_file(os.path.join("setuptools", "flake.nix.tmpl"))

def flake_nix_poetry_template() -> str:
    return read_resource_file(os.path.join("poetry", "package.nix.tmpl"))

def resolve_flake_nix_template(package_type: str):
    mapping = {
        "poetry": flake_nix_poetry_template,
        "setuptools": flake_nix_setuptools_template
    }

    result = mapping.get(package_type, None)
    if not result:
        result = flake_nix_setuptools_template

    return result()

def package_nix_setuptools_pypi_template() -> str:
    return read_resource_file(os.path.join("setuptools", "pypi", "package.nix.tmpl"))

def package_nix_setuptools_github_template() -> str:
    return read_resource_file(os.path.join("setuptools", "github", "package.nix.tmpl"))

def package_nix_poetry_template() -> str:
    return read_resource_file(os.path.join("poetry", "package.nix.tmpl"))

def resolve_package_nix_template(package_type: str) -> str:
    mapping = {
        "poetry": package_nix_poetry_template,
        "setuptools": package_nix_setuptools_github_template
    }
    result = mapping.get(package_type, None)
    if not result:
        result = package_nix_setuptools_github_template

    return result()

def is_flake(dep: Dict[str, str]) -> bool:
    return dep.get("flake_url", "") != ""

def extract_dep_templates_for_flake_nix(inputs: Dict[str, str]) -> (str, str, str):
    if inputs:
        flakes_declaration = "\n  ".join(f'{dep["name"]}-flake.url = "{dep.get("flake_url", "")}";' for dep in inputs if is_flake(dep))
        not_flakes_with_newlines = "\n            ".join(f'{extract_name_from_nixpkgs_package(dep["name"])} = {dep["name"]};' for dep in inputs if not is_flake(dep))
        flakes_with_newlines = "\n            ".join(f'{dep["name"]} = {dep["name"]}-flake.packages.${{system}}.{dep["name"]};' for dep in inputs if is_flake(dep))
    else:
        flakes_declaration = ""
        not_flakes_with_newlines = ""
        flakes_with_newlines = ""
    return (flakes_declaration, not_flakes_with_newlines, flakes_with_newlines)

def extract_dep_templates_for_package_nix(inputs: List[Dict[str, str]]) -> (str, str, str):
    if inputs:
        with_commas = ", ".join(extract_name_from_nixpkgs_package(dep["name"]) for dep in inputs)
        with_blanks = "".join(extract_name_from_nixpkgs_package(dep["name"]) for dep in inputs)
        declaration = f", {with_commas}"
    else:
        with_commas = ""
        with_blanks = ""
        declaration = ""
    return (with_commas, with_blanks, declaration)

def create_nix_file(template: str, base_folder: str, package_info: Dict[str, str], github_info: Dict[str, str]):

    package_name = package_info["name"]
    package_version = package_info["version"]
    folder_name = f"{package_name}-{package_version}"
    package_folder = Path(base_folder) / folder_name
    if not os.path.exists(package_folder):
        os.makedirs(package_folder)
    flake_nix_path = f"{package_folder}/flake.nix"
    package_nix_path = f"{package_folder}/{package_name}-{package_version}.nix"

    package_license = pypi_license_to_nix_license(package_info["license"])
    package_description = extract_description(package_info.get("description", ""), package_info.get("description_content_type", ""))
    package_repo = package_info["github_url"]

    package_metadata = package_info.get("metadata", {})
    native_build_inputs_flakes_declaration, native_build_inputs_not_flakes_with_newlines, native_build_inputs_flakes_with_newlines = extract_dep_templates_for_flake_nix(package_metadata.get("native_build_inputs", []))
    propagated_build_inputs_flakes_declaration, propagated_build_inputs_not_flakes_with_newlines, propagated_build_inputs_flakes_with_newlines = extract_dep_templates_for_flake_nix(package_metadata.get("propagated_build_inputs", []))
    build_inputs_flakes_declaration, build_inputs_not_flakes_with_newlines, build_inputs_flakes_with_newlines = extract_dep_templates_for_flake_nix(package_metadata.get("build_inputs", []))
    native_build_inputs_with_commas, native_build_inputs_with_blanks, native_build_inputs_declaration = extract_dep_templates_for_package_nix(package_metadata.get("native_build_inputs", []))
    propagated_build_inputs_with_commas, propagated_build_inputs_with_blanks, propagated_build_inputs_declaration = extract_dep_templates_for_package_nix(package_metadata.get("propagated_build_inputs", []))
    build_inputs_with_commas, build_inputs_with_blanks, build_inputs_declaration = extract_dep_templates_for_package_nix(package_metadata.get("build_inputs", []))

    if not os.path.exists(flake_nix_path):
        with open(flake_nix_path, "w") as f:
            f.write(template.format(
                package_name=package_name,
                package_version=package_version,
                package_version_with_underscores=package_version.replace(".", "_"),
                package_description=package_description,
                package_license=package_license,
                package_repo=package_repo,
                native_build_inputs_flakes_declaration=native_build_inputs_flakes_declaration,
                native_build_inputs_not_flakes_with_newlines=native_build_inputs_not_flakes_with_newlines,
                native_build_inputs_flakes_with_newlines=native_build_inputs_flakes_with_newlines,
                propagated_build_inputs_flakes_declaration=propagated_build_inputs_flakes_declaration,
                propagated_build_inputs_not_flakes_with_newlines=propagated_build_inputs_not_flakes_with_newlines,
                propagated_build_inputs_flakes_with_newlines=propagated_build_inputs_flakes_with_newlines,
                build_inputs_flakes_declaration=build_inputs_flakes_declaration,
                build_inputs_not_flakes_with_newlines=build_inputs_not_flakes_with_newlines,
                build_inputs_flakes_with_newlines=build_inputs_flakes_with_newlines,
                native_build_inputs_declaration=native_build_inputs_declaration,
                native_build_inputs_with_blanks=native_build_inputs_with_blanks,
                propagated_build_inputs_declaration=propagated_build_inputs_declaration,
                propagated_build_inputs_with_blanks=propagated_build_inputs_with_blanks,
                build_inputs_declaration=build_inputs_declaration,
                build_inputs_with_blanks=build_inputs_with_blanks
            ))

def create_flake_nix_file(base_folder: str, package_info: Dict[str, str], github_info: Dict[str, str]):
    create_nix_file(resolve_flake_nix_template(package_info["type"]), base_folder, package_info, github_info)

def create_package_nix_file(base_folder: str, package_info: Dict[str, str], github_info: Dict[str, str]):
    create_nix_file(resolve_package_nix_template(package_info["type"]), base_folder, package_info, github_info)
