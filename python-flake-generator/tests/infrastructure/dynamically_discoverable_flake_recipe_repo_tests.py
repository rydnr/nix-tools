import sys
from pathlib import Path

base_folder = str(Path(__file__).resolve().parent.parent.parent / 'src')
if base_folder not in sys.path:
    sys.path.append(base_folder)

from domain.flake import Flake
from infrastructure.dynamically_discoverable_flake_recipe_repo import DynamicallyDiscoverableFlakeRecipeRepo

import unittest

class DynamicallyDiscoverableFlakeRecipeRepoTests(unittest.TestCase):
    def test_extract_requires(self):
        sut = DynamicallyDiscoverableFlakeRecipeRepo()
        self.assertIsNotNone(
            sut.find_by_flake(Flake("pytest-asyncio", "0.19.0", None, [], [], [], []))
        )

if __name__ == "__main__":
    unittest.main()
