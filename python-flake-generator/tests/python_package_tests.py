import sys
sys.path.insert(0, "domain")

import unittest

from python_package import PythonPackage

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
