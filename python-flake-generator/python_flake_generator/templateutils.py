#!/usr/bin/env python3

import os
from pathlib import Path
from typing import Dict, List

def resolve_create_flake_nix_file(package_type: str):
    mapping = {
        "poetry": create_flake_nix_poetry_file,
        "setuptools": create_flake_nix_setuptools_file
    }
    if mapping[package_type]:
        return mapping[package_type]
    else:
        return create_flake_nix_setuptools_file

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

def create_flake_nix_setuptools_file(base_folder: str, package_info: Dict[str, str], github_info: Dict[str, str]):

    package_name = package_info["name"]
    package_version = package_info["version"]
    folder_name = f"{package_name}-{package_version}"
    package_folder = Path(base_folder) / folder_name
    if not os.path.exists(package_folder):
        os.makedirs(package_folder)
    flake_nix_path = f"{package_folder}/flake.nix"
    package_nix_path = f"{package_folder}/{package_name}-{package_version}.nix"

    package_license = pypi_license_to_nix_license(package_info["license"])
    package_description = package_info.get("description", "").strip(" \n\t")
    package_repo = package_info["github_url"]

    package_metadata = package_info.get("metadata", {})
    native_build_inputs_flakes_declaration, native_build_inputs_not_flakes_with_newlines, native_build_inputs_flakes_with_newlines = extract_dep_templates_for_flake_nix(package_metadata.get("native_build_inputs", []))
    propagated_build_inputs_flakes_declaration, propagated_build_inputs_not_flakes_with_newlines, propagated_build_inputs_flakes_with_newlines = extract_dep_templates_for_flake_nix(package_metadata.get("propagated_build_inputs", []))
    build_inputs_flakes_declaration, build_inputs_not_flakes_with_newlines, build_inputs_flakes_with_newlines = extract_dep_templates_for_flake_nix(package_metadata.get("build_inputs", []))

    flake_nix_template = "" # setuptools/flake.nix.tmpl

    if not os.path.exists(flake_nix_path):
        with open(flake_nix_path, "w") as f:
            f.write(flake_nix_template.format(
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
                build_inputs_flakes_with_newlines=build_inputs_flakes_with_newlines
            ))

def create_flake_nix_poetry_file(base_folder: str, package_info: Dict[str, str], github_info: Dict[str, str]):

    package_name = package_info["name"]
    package_version = package_info["version"]
    folder_name = f"{package_name}-{package_version}"
    package_folder = Path(base_folder) / folder_name
    if not os.path.exists(package_folder):
        os.makedirs(package_folder)
    flake_nix_path = f"{package_folder}/flake.nix"
    package_nix_path = f"{package_folder}/{package_name}-{package_version}.nix"

    package_license = pypi_license_to_nix_license(package_info["license"])
    package_description = package_info.get("description", "").strip(" \n\t")
    package_repo = package_info["github_url"]

    package_metadata = package_info.get("metadata", {})
    native_build_inputs_flakes_declaration, native_build_inputs_not_flakes_with_newlines, native_build_inputs_flakes_with_newlines = extract_dep_templates_for_flake_nix(package_metadata.get("native_build_inputs", []))
    propagated_build_inputs_flakes_declaration, propagated_build_inputs_not_flakes_with_newlines, propagated_build_inputs_flakes_with_newlines = extract_dep_templates_for_flake_nix(package_metadata.get("propagated_build_inputs", []))
    build_inputs_flakes_declaration, build_inputs_not_flakes_with_newlines, build_inputs_flakes_with_newlines = extract_dep_templates_for_flake_nix(package_metadata.get("build_inputs", []))

    flake_nix_template = "" # poetry/flake.nix.tmpl

    if not os.path.exists(flake_nix_path):
        with open(flake_nix_path, "w") as f:
            f.write(flake_nix_template.format(
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
                build_inputs_flakes_with_newlines=build_inputs_flakes_with_newlines
            ))

def create_flake_nix_file(base_folder: str, package_info: Dict[str, str], github_info: Dict[str, str]):
    create_flake_nix = resolve_create_flake_nix_file(package_info["type"])
    create_flake_nix(base_folder, package_info, github_info)

def resolve_create_package_nix_template(package_type: str) -> str:
    mapping = {
        "poetry": package_nix_poetry_template,
        "setuptools": package_nix_setuptools_template
    }
    if mapping[package_type]:
        return mapping[package_type]
    else:
        return package_nix_setuptools_file

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

def package_nix_setuptools_pypi_file_template() -> str:
    return "" # setuptools/pypi/package.nix.tmpl

def package_nix_setuptools_github_file_template() -> str:
    return "" # setuptools/github/package.nix.tmpl

def package_nix_poetry_file() -> str:
    return "" # poetry/package.nix.tmpl

def create_package_nix_setuptools_file(base_folder: str, package_info: Dict[str, str], github_info: Dict[str, str]):

    package_name = package_info["name"]
    package_version = package_info["version"]
    folder_name = f"{package_name}-{package_version}"
    package_folder = Path(base_folder) / folder_name
    if not os.path.exists(package_folder):
        os.makedirs(package_folder)
    flake_nix_path = f"{package_folder}/flake.nix"
    package_nix_path = f"{package_folder}/{package_name}-{package_version}.nix"

    package_license = pypi_license_to_nix_license(package_info["license"])
    package_description = package_info.get("description", "").strip(" \n\t")
    package_repo = package_info["github_url"]
    package_hash = package_info["hash"]
    if not package_hash:
        package_hash = package_info["sha256"]
    repo_owner = package_info.get("repo_owner", "")
    if not repo_owner:
        if package_repo:
            repo_owner, repo_name = extract_owner_and_repo_name(package_repo)


    package_metadata = package_info.get("metadata", {})
    native_build_inputs_with_commas, native_build_inputs_with_blanks, native_build_inputs_declaration = extract_dep_templates_for_package_nix(package_metadata.get("native_build_inputs", []))
    propagated_build_inputs_with_commas, propagated_build_inputs_with_blanks, propagated_build_inputs_declaration = extract_dep_templates_for_package_nix(package_metadata.get("propagated_build_inputs", []))
    build_inputs_with_commas, build_inputs_with_blanks, build_inputs_declaration = extract_dep_templates_for_package_nix(package_metadata.get("build_inputs", []))

    package_nix_template = retrieve_package_nix_file(package_info, github_info)

    if not os.path.exists(package_nix_path):
        with open(package_nix_path, "w") as f:
            f.write(package_nix_template.format(
                package_name=package_name,
                package_version=package_version,
                package_hash=package_hash,
                package_description=package_description,
                package_license=package_license,
                package_repo=package_repo,
                native_build_inputs_declaration=native_build_inputs_declaration,
                native_build_inputs_with_blanks=native_build_inputs_with_blanks,
                propagated_build_inputs_declaration=propagated_build_inputs_declaration,
                propagated_build_inputs_with_blanks=propagated_build_inputs_with_blanks,
                build_inputs_declaration=build_inputs_declaration,
                build_inputs_with_blanks=build_inputs_with_blanks
            ))

def create_package_nix_file(base_folder: str, package_info: Dict[str, str], github_info: Dict[str, str]):
    create_package_nix = resolve_create_package_nix_file(package_info["type"])
    create_package_nix(base_folder, package_info, github_info)
