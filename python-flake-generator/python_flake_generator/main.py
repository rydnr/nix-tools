#!/usr/bin/env python3
from typing import Dict, List
import logging

from packagetypeutils import get_package_type
from pypiutils import get_pypi_info
from nixutils import get_nix_prefetch_git_hash, extract_name_from_nixpkgs_package, is_python_package_in_nixpkgs
from githubutils import get_github_info, extract_owner_and_repo_name
from licenseutils import pypi_license_to_nix_license
from poetryutils import load_poetry_lock
from templateutils import create_flake_nix_file, create_package_nix_file
from cliutils import cli_args

def get_missing_packages(poetry_lock, missing_packages_list):
    package_data = {}
    for package in poetry_lock["package"]:
        package_name = package["name"]
        if package_name in missing_packages_list:
            package_data[package_name] = package["version"]
    return package_data

def extract_package_names(poetry_lock) -> List[str]:
    package_names = []
    for package in poetry_lock["package"]:
        package_names.append(package["name"])
    return package_names

def main():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    args = cli_args()

    poetry_lock = load_poetry_lock(args.poetryLockFile)

    package_names = extract_package_names(poetry_lock)

    not_in_nixpkgs = []

    for package_name in package_names:
        if not is_python_package_in_nixpkgs(package_name):
            not_in_nixpkgs.append(package_name)

    missing_packages = get_missing_packages(poetry_lock, not_in_nixpkgs)

    for package_name, version_spec in missing_packages.items():
        package_info = get_pypi_info(package_name, version_spec)
        github_info = get_github_info(args.githubToken, package_info["github_url"], package_info["rev"])
        package_type = get_package_type(args.githubToken, package_info["github_url"], package_info["rev"])
        logging.debug(f"package type: {package_type}")
        create_flake_nix_file(args.baseFolder, package_type, package_info, github_info)
        create_package_nix_file(args.baseFolder, package_type, package_info, github_info)
        break

if __name__ == "__main__":
    main()
