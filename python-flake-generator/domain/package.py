#!/usr/bin/env python3

from github import get_file_contents_in_github_repo, file_exists_in_github_repo

from typing import Dict
import logging

import toml

def parse_toml(contents: str):
    logging.debug(contents)
    return toml.loads(contents)

def get_package_type(github_token: str, github_url: str, rev: str) -> str:
    result = "setuptools"
    if not github_url:
        return result

    if file_exists_in_github_repo(github_token, github_url, rev, "pyproject.toml"):
        pyprojecttoml = parse_toml(get_file_contents_in_github_repo(github_token, github_url, rev, "pyproject.toml"))

        build_system_requires = pyprojecttoml.get("build-system", {}).get("requires", [])
        if any(item.startswith("poetry") for item in build_system_requires):
            result = "poetry"
        elif any(item.startswith("flit") for item in build_system_requires):
            result = "flit"
    elif file_exists_in_github_repo(github_token, github_url, rev, "Pipfile"):
        result = "pipenv"

    return result
