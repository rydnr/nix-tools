import sys
from pathlib import Path

base_folder = str(Path(__file__).resolve().parent.parent)
if base_folder not in sys.path:
    sys.path.append(base_folder)

from domain.resource_repo import ResourceRepo

class FilesystemResourceRepo(ResourceRepo):
    """
    A ResourceRepo that uses the filesystem as store
    """
    def __init__(self):
        super().__init__()

    def find_by_path(filePath: str) -> str:
        base_dir = os.path.dirname(os.path.realpath(__file__))
        resources_dir = os.path.join(base_dir, "..", "resources")
        file = os.path.join(resources_dir, filePath)

        content = ""
        with open(file, "r") as fileDesc:
            content = fileDesc.read()

        return content

    def read_resource_json(filePath: str) -> Dict:
        base_dir = os.path.dirname(os.path.realpath(__file__))
        resources_dir = os.path.join(base_dir, "..", "resources")
        json_file = os.path.join(resources_dir, filePath)

        with open(json_file, "r") as file:
            config = json.load(file)
