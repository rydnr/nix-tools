from domain.event import Event
from domain.python.python_package import PythonPackage

class PythonPackageCreated(Event):
    """
    Represents the event when a PythonPackage has been created.
    """

    def __init__(self, package: PythonPackage):
        """Creates a new PythonPackageCreated instance"""
        self._package = package

    @property
    def package(self):
        return self._package

    def __str__(self):
        return f'{{ "name": "{__name__}", "package": "{self._package}" }}'
