#!/usr/bin/env python3

import toml

class Poetry():
    def load_poetry_lock(filepath):
        with open(filepath, "r") as f:
            return toml.load(f)
