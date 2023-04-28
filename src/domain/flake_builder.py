from domain.flake_recipe import FlakeRecipe
from domain.flake_built import FlakeBuilt
from domain.flake_build.git_add_failed import GitAddFailed
from domain.flake_build.git_init_failed import GitInitFailed
from domain.flake_build.nix_build_failed import NixBuildFailed

import os
import shutil

class FlakeBuilder():

    def __init__(self, flakeRecipe: FlakeRecipe):
        """Creates a new flake recipe instance"""
        super().__init__(id)
        self._flake_recipe = flakeRecipe

    @property
    @primary_key_attribute
    def flake_recipe(self) -> str:
        return self._flake_recipe

    @classmethod
    def build_flake(cls, command: BuildFlake) -> FlakeBuilt:
        result = None

        with tempfile.TemporaryDirectory() as temp_dir:
            self.copy_folder_contents(folder, temp_dir)
            self.git_init(temp_dir)
            for file in os.listdir(temp_dir):
                self.git_add(temp_dir, file)
            self.nix_build(temp_dir)

        return FlakeBuilt(command.package_name, command.package_version, command.flake_folder)

    def copy_folder_contents(self, source: str, destination: str):
        logging.getLogger(__name__).debug(f'Copying {folder} contents to a temporary folder')
        shutil.copytree(folder, temp_dir)

    def git_init(self, folder: str):
        output = None
        try:
            logging.getLogger(__name__).debug(f'Initializing a git repository in {folder}')
            output = subprocess.check_output(['git', 'init'], stderr=subprocess.STDOUT, cwd=folder)
        except subprocess.CalledProcessError:
            raise GitInitFailed(folder, output.stdout)

    def git_add(self, folder: str, file: str):
        logging.getLogger(__name__).debug(f'Adding {file} to the git repository in {folder}')
        output = None
        try:
            output = subprocess.check_output(['git', 'add', file], stderr=subprocess.STDOUT, cwd=folder)
        except subprocess.CalledProcessError:
            raise GitAddFailed(file, output.stdout)

    def nix_build(self, folder: str):
        output = None
        try:
            logging.getLogger(__name__).debug(f'Building the flake in {folder}')
            output = subprocess.check_output(['nix', 'build', '.'], stderr=subprocess.STDOUT, cwd=folder)
        except subprocess.CalledProcessError:
            raise NixBuildFailed(folder, output.stdout)
