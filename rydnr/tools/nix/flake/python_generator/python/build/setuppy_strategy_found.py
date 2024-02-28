from domain.python.python_package import PythonPackage
from domain.python.python_package_base_event import PythonPackageBaseEvent
from domain.value_object import attribute


class SetuppyStrategyFound(PythonPackageBaseEvent):
    """
    Represents the event triggered when a Python package can be built using setup.py.
    """

    def __init__(self, pythonPackage: PythonPackage):
        """Creates a new PythonBuildStrategyRequested instance"""
        super().__init__(pythonPackage.name, pythonPackage.version, pythonPackage.git_repo)
        self._pythonPackage = pythonPackage

    @property
    @attribute
    def pythonPackage() -> PythonPackage:
        return self._pythonPackage
