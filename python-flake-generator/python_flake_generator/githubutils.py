#!/usr/bin/env python3

import re
import requests
from typing import Dict

from nixutils import get_nix_prefetch_git_hash

def get_github_info(github_token: str, github_url: str, rev: str) -> Dict[str, str]:
    if not github_url:
        return {"description": "", "license": ""}

    repo_path = github_url.split("github.com/")[-1].rstrip("/")
    headers = {"Authorization": f"token {github_token}"}
    repo_info = requests.get(f"https://api.github.com/repos/{repo_path}", headers=headers).json()
    license = repo_info.get("license", {}).get("spdx_id", "")

    readme_info = requests.get(f"https://api.github.com/repos/{repo_path}/readme", headers=headers).json()
    readme_text = requests.get(readme_info["download_url"]).text
    description = readme_text.split("\n")[0].strip(" \n\t")
    hash = get_nix_prefetch_git_hash(github_url, rev)
    return {"description": description, "license": license, "sha256": hash}

def extract_owner_and_repo_name(github_repo_url: str) -> tuple:
    pattern = r"(?:https?://)?(?:www\.)?github\.com/([^/]+)/([^/]+)"
    try:
        match = re.match(pattern, github_repo_url)
        owner, repo_name = match.groups()
        return owner, repo_name

    except:
        print(f"Invalid repo: {github_repo_url}")
