#!/usr/bin/env python3

from description import extract_description
from nix import get_nix_prefetch_git_hash
import re
import requests
import base64
from typing import Dict

def get_github_info(github_token: str, github_url: str, rev: str) -> Dict[str, str]:
    if not github_url:
        return {"description": "", "license": ""}

    owner, repo_name = extract_owner_and_repo_name(github_url)
    headers = {"Authorization": f"token {github_token}"}
    repo_info = requests.get(f"https://api.github.com/repos/{owner}/{repo_name}", headers=headers).json()
    license = repo_info.get("license", {}).get("spdx_id", "")

    description_info = repo_info.get("description", None)
    description = ""
    if description_info:
        description = extract_description(description_info, "text/plain")

    hash = get_nix_prefetch_git_hash(github_url, rev)
    return {"description": description, "license": license, "hash": hash}

def extract_owner_and_repo_name(github_repo_url: str) -> tuple:
    pattern = r"(?:https?://)?(?:www\.)?github\.com/([^/]+)/([^/]+)"
    try:
        match = re.match(pattern, github_repo_url)
        owner, repo_name = match.groups()
        return owner, repo_name

    except:
        print(f"Invalid repo: {github_repo_url}")

def request_file_in_github_repo(github_token: str, github_url: str, rev: str, file: str) -> bool:
    headers = {"Authorization": f"token {github_token}", "Accept": "application/vnd.github+json"}

    owner, repo_name = extract_owner_and_repo_name(github_url)
    return requests.get(f"https://api.github.com/repos/{owner}/{repo_name}/contents/{file}?ref={rev}", headers=headers)

def file_exists_in_github_repo(github_token: str, github_url: str, rev: str, file: str) -> bool:
    file_info = request_file_in_github_repo(github_token, github_url, rev, file)

    return file_info.status_code == 200


def get_file_contents_in_github_repo(github_token: str, github_url: str, rev: str, file: str) -> str:
    file_info = request_file_in_github_repo(github_token, github_url, rev, file)

    if (file_info.status_code == 200):
        decoded_bytes = base64.b64decode(file_info.json().get("content", ""))
        return decoded_bytes.decode('utf-8')
    else:
        return ""
