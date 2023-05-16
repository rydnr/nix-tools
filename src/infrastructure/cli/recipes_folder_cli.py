from domain.primary_port import PrimaryPort

import argparse
import os
from pathlib import Path

class RecipesFolderCli(PrimaryPort):

    """
    A PrimaryPort that configures the recipes folder from the command line.
    """

    def __init__(self):
        super().__init__()

    def priority(self) -> int:
        return 2

    async def accept(self, app):

        parser = argparse.ArgumentParser(
            description="Parses the folder with the custom flakes"
        )
        parser.add_argument(
            "-r", "--recipes_folder", required=False, help="The flakes folder"
        )
        args, unknown_args = parser.parse_known_args()
        recipes_folder = args.recipes_folder
        if not recipes_folder:
            recipes_folder = os.path.join(str(Path(__file__).resolve().parent.parent.parent.parent), "recipes")
        await app.accept_recipes_folder(recipes_folder)
