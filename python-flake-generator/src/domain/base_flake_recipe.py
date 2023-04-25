import sys
from pathlib import Path

base_folder = str(Path(__file__).resolve().parent.parent)
if base_folder not in sys.path:
    sys.path.append(base_folder)

from domain.flake_recipe import FlakeRecipe
from domain.flake import Flake
from domain.flake_created_event import FlakeCreated
from domain.ports import Ports

class BaseFlakeRecipe(FlakeRecipe):

    """
    Represents a base nix flake recipe.
    """
    def __init__(self, flake: Flake):
        """Creates a new base nix flake recipe instance"""
        super().__init__(id)
        self._flake = flake

    @classmethod
    def matches(cls, flake):
        return True

    def process(self) -> FlakeCreated:
        flake_nix = self.flake_nix(self.flake)
        package_nix = self.package_nix(self.flake)
        return Ports.instance().resolveFlakeRepo().create(
            self.flake,
            [
                {
                    "contents": flake_nix["contents"],
                    "path": os.path.join(flake_nix["folder"], flake_nix["path"])
                }, {
                    "contents": package_nix["contents"],
                    "path": os.path.join(package_nix["folder"], package_nix["path"])
                }
            ])

    def flake_nix(self, flake: Flake) -> str:
        template = Ports.instance().resolveNixTemplateRepo().find_flake_template_by_type(flake.name, flake.version, flake.python_package.get_package_type())
        return { "contents": template.render(flake), "folder": template.folder, "path": template.path }

    def package_nix(self, flake: Flake) -> str:
        template = Ports.instance().resolveNixTemplateRepo().find_package_template_by_type(flake.name, flake.version, flake.python_package.get_package_type())
        return { "contents": template.render(flake), "folder": template.folder, "path": template.path }
