#!/usr/bin/env python3
import argparse

def cli_args():
    parser = argparse.ArgumentParser(description="Generates flakes from templates for packages in poetry.lock not available in nixpkgs")
    parser.add_argument("poetryLockFile", help="The poetry.lock file")
    parser.add_argument("baseFolder", help="The base folder for the flakes")
    parser.add_argument("githubToken", help="The github token")
    return parser.parse_args()
