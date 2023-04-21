import sys

sys.path.insert(0, "domain")
from resource_repo import ResourceRepo

class FilesystemResourceRepo(ResourceRepo):

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
