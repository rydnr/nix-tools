from entity import Entity, primary_key_attribute, attribute


class PythonPackage(Entity):
    """
    Represents a Python package.
    """
    def __init__(self, name, version):
        """Creates a new PythonPackage instance"""
        super().__init__(id)
        self._name = name
        self._version = version


    @property
    @primary_key_attribute
    def name(self):
        return self._name


    @property
    @primary_key_attribute
    def version(self):
        return self._version
