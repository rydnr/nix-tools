import sys
from pathlib import Path

base_folder = str(Path(__file__).resolve().parent.parent.parent / 'src')
if base_folder not in sys.path:
    sys.path.append(base_folder)

import domain
from domain.python_package import PythonPackage

import unittest

class PythonPackageTests(unittest.TestCase):
    def test_extract_requires(self):
        sut = PythonPackage("dummy", "0.1", {}, {})
        self.assertEqual(
            sut.extract_requires("setuptools>=51"),
            ("setuptools", "", "51", ">=51")
        )
        self.assertEqual(
            sut.extract_requires("wheel>=0.36"),
            ("wheel", "", "0.36", ">=0.36")
        )
        self.assertEqual(
            sut.extract_requires("setuptools_scm[toml]>=6.2"),
            ("setuptools_scm", "toml", "6.2", ">=6.2")
        )

if __name__ == '__main__':
    unittest.main()
