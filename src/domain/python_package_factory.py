from domain.python_package import PythonPackage
from domain.unsupported_python_package import UnsupportedPythonPackage

import logging
from typing import Dict

class PythonPackageFactory():
    """
    It's responsible for creating PythonPackage instances.
    """
    @classmethod
    def create(cls, name: str, version: str, info: Dict, release: Dict) -> PythonPackage:
        """Creates a PythonPackage matching given name and version."""
        result = None
        git_repo = PythonPackage.extract_repo(version, info)
        if not git_repo:
            logging.getLogger(__name__).warn(f'No repository url found for {name}-{version}')
        else:
            for python_package_class in PythonPackage.__subclasses__():
                if python_package_class.git_repo_matches(git_repo):
                    result = python_package_class(name, version, info, release, git_repo)
                    break

        if not result:
            raise UnsupportedPythonPackage(name, version)

        return result
