#!/usr/bin/env python3

import subprocess
import re

def get_nix_prefetch_git_hash(url, tag):
    # Use nix-prefetch-git to compute the hash
    result = subprocess.run(['nix-prefetch-git', '--deepClone', f'{url}/tree/{tag}'], check=True, capture_output=True, text=True)
    output = result.stdout

    return output.splitlines()[-1]

def extract_name_from_nixpkgs_package(pkg: str) -> str:
    result = pkg
    match = re.search(r'[^.]+$|$', pkg)
    if match:
        result = match.group()
    return result

def is_python_package_in_nixpkgs(package_name: str) -> bool:
    try:
        result = subprocess.run(
            [
                "nix-instantiate",
                "--eval",
                "--expr",
                f"with import <nixpkgs> {{ }}; builtins.hasAttr \"{package_name}\" python3Packages",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip() == "true"
    except subprocess.CalledProcessError:
        return False
