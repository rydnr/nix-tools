from domain.event import Event
from domain.event_listener import EventListener
from domain.flake_build.git_add_failed import GitAddFailed
from domain.flake_build.git_init_failed import GitInitFailed
from domain.flake_build.nix_build_failed import NixBuildFailed
from domain.flake_built import FlakeBuilt
from domain.flake_created import FlakeCreated
from domain.flake_recipe import FlakeRecipe

import os
import shutil
from typing import List, Type

class FlakeBuilder(EventListener):

    @classmethod
    def supported_events(cls) -> List[Type[Event]]:
        """
        Retrieves the list of supported event classes.
        """
        return [ FlakeCreated ]


    def listenFlakeCreated(self, event: FlakeCreated) -> FlakeBuilt:
        result = None

        with tempfile.TemporaryDirectory() as temp_dir:
            self.copy_folder_contents(folder, temp_dir)
            self.git_init(temp_dir)
            for file in os.listdir(temp_dir):
                self.git_add(temp_dir, file)
            self.nix_build(temp_dir)

        return FlakeBuilt(event.package_name, event.package_version, event.flake_folder)

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
