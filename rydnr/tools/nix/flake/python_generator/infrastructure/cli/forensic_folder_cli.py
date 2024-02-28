from domain.primary_port import PrimaryPort

import argparse


class ForensicFolderCli(PrimaryPort):

    """
    A PrimaryPort that configures the forensic folder from the command line.
    """

    def __init__(self):
        super().__init__()

    def priority(self) -> int:
        return 1

    async def accept(self, app):

        parser = argparse.ArgumentParser(
            description="Parses the forensic folder"
        )
        parser.add_argument(
            "-x", "--forensic_folder", required=True, help="The folder where to copy the contents of flakes whose build failed"
        )
        args, unknown_args = parser.parse_known_args()
        await app.accept_forensic_folder(args.forensic_folder)
