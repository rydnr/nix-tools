import json
import os
from typing import Dict

class ResourceFiles():

    def __init__(self):
        super().__init__()
        _singleton = None

    @classmethod
    def initialize(cls):
        cls._singleton = ResourceFiles()

    @classmethod
    def instance(cls):
        return cls._singleton

    def read_resource_file(self, filePath: str) -> str:
        base_dir = os.path.dirname(os.path.realpath(__file__).parent.parent.parent)
        resources_dir = os.path.join(base_dir, "resources")
        metadata_json = os.path.join(resources_dir, filePath)

        with open(metadata_json, "r") as file:
            content = file.read()

        return content

    def read_resource_json(self, filePath: str) -> Dict:
        base_dir = os.path.dirname(os.path.realpath(__file__).parent.parent.parent)
        resources_dir = os.path.join(base_dir, "resources")
        json_file = os.path.join(resources_dir, filePath)

        with open(json_file, "r") as file:
            config = json.load(file)

        return config

ResourceFiles.initialize()
