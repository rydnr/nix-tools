#!/usr/bin/env python3

import json
import os
from typing import Dict

def read_resource_file(filePath: str) -> str:
    base_dir = os.path.dirname(os.path.realpath(__file__))
    resources_dir = os.path.join(base_dir, "..", "resources")
    metadata_json = os.path.join(resources_dir, filePath)

    with open(metadata_json, "r") as file:
        content = file.read()

    return content

def read_resource_json(filePath: str) -> Dict:
    base_dir = os.path.dirname(os.path.realpath(__file__))
    resources_dir = os.path.join(base_dir, "..", "resources")
    json_file = os.path.join(resources_dir, filePath)

    with open(json_file, "r") as file:
        config = json.load(file)
