#!/usr/bin/env python3

from description import extract_description
from resources import read_resource_json

import logging
from packaging.specifiers import SpecifierSet
import re
import requests
from typing import Dict

class Pypi():
    def get_pypi_info(package_name: str, version_spec: str) -> Dict[str, str]:
        # If the version_spec is an exact version, add '==' before it
        if re.match(r"^\d+(\.\d+)*(-?(rc|b)\d+)?$", version_spec):
            version_spec = f"=={version_spec}"

            specifier_set = SpecifierSet(version_spec)

            logging.debug(f"Retrieving {package_name}{version_spec} info from https://pypi.org/pypi/{package_name}/json")
            package_data = requests.get(f"https://pypi.org/pypi/{package_name}/json").json()
            versions = package_data["releases"].keys()

            compatible_versions = [v for v in versions if v in specifier_set]

        if not compatible_versions:
            raise Exception(f"No compatible versions found for {package_name} with spec {version_spec}")

        latest_version = max(compatible_versions)
        latest_release = len(package_data["releases"][latest_version]) - 1
        release_info = package_data["releases"][latest_version][latest_release]
        package_info = package_data["info"]
        github_url = ""
        project_urls = package_info["project_urls"]
        sha256 = ""
        digests = release_info["digests"]
        if digests:
            sha256 = digests["sha256"]

        description = extract_description(package_info["description"], package_info["description_content_type"])

        config = read_resource_json("metadata.json")

        package_metadata_all_versions = []

        if config:
            package_metadata_all_versions = config.get(package_name, None)

        if not package_metadata_all_versions:
            package_metadata_all_versions = []

        version_filter = lambda x: x.get("version", "") == latest_version

        matching_version = [x for x in package_metadata_all_versions if version_filter(x)]

        package_metadata = matching_version[0] if matching_version else {}

        github_url = package_metadata.get("github_url", "")

        if not github_url and project_urls:
            github_url = project_urls.get("Repository")

        return {
            "name": package_name,
            "version": latest_version,
            "url": release_info["url"],
            "hash": sha256,
            "github_url": github_url,
            "description": description,
            "license": package_info["license"],
            "rev": package_metadata.get("rev", f"v{latest_version}"),
            "metadata": package_metadata
        }
