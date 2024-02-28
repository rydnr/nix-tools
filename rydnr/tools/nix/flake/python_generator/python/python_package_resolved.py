from domain.python.python_package import PythonPackage
from domain.python.python_package_base_event import PythonPackageBaseEvent
from domain.value_object import attribute


class PythonPackageResolved(PythonPackageBaseEvent):
    """
    Represents the event when a Python project has been fully resolved.
    """

    def __init__(self, packageName: str, packageVersion: str, pythonPackage: PythonPackage):
        """Creates a new PythonPackageResolved instance"""
        super().__init__(packageName, packageVersion, pythonPackage.git_repo)
        self._python_package = pythonPackage

    @property
    @attribute
    def python_package() -> PythonPackage:
        return self._python_package
