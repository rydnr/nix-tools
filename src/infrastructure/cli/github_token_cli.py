from domain.primary_port import PrimaryPort

import argparse

class GithubTokenCli(PrimaryPort):

    """
    A PrimaryPort that configures the github token from the command line.
    """

    def __init__(self):
        super().__init__()

    def priority(self) -> int:
        return 0

    def accept(self, app):

        parser = argparse.ArgumentParser(
            description="Parses the github token from the command line"
        )
        parser.add_argument("-t", "--github_token", required=True, help="The github token")
        args, unknown_args = parser.parse_known_args()
        app.accept_github_token(args.github_token)
