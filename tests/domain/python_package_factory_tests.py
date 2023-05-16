import sys
from pathlib import Path

base_folder = str(Path(__file__).resolve().parent.parent.parent / 'src')
if base_folder not in sys.path:
    sys.path.append(base_folder)

from domain.python_package_factory import PythonPackageFactory

import unittest
from unittest.mock import MagicMock
import asyncio

class PythonPackageFactoryTests(unittest.IsolatedAsyncioTestCase):
    async def test_create(self):
        factory = PythonPackageFactory()

        # Mock the _emit_git_repo_requested method to make the test more predictable
        factory._emit_git_repo_requested = MagicMock(return_value=asyncio.Future())
        factory._emit_git_repo_requested.return_value.set_result(None)

        # Run the create method
        package = await factory.create("beautifulsoup4", "4.9.3", {}, {})

        # Ensure that the _check_requested method was called
        factory._emit_git_repo_requested.assert_called_once()

        # Ensure that the create method returned the correct package
        self.assertTrue(package is not None, "PythonPackage is none")


if __name__ == '__main__':
    unittest.main()
