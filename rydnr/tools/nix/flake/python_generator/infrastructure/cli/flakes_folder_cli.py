from domain.primary_port import PrimaryPort

import argparse

class FlakesFolderCli(PrimaryPort):

    """
    A PrimaryPort that configures the flakes folder from the command line.
    """

    def __init__(self):
        super().__init__()

    def priority(self) -> int:
        return 1

    async def accept(self, app):

        parser = argparse.ArgumentParser(
            description="Parses the folder with the custom flakes"
        )
        parser.add_argument(
            "-f", "--flakes_folder", required=True, help="The flakes folder"
        )
        args, unknown_args = parser.parse_known_args()
        await app.accept_flakes_folder(args.flakes_folder)
