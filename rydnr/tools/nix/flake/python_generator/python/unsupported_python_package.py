class UnsupportedPythonPackage(Exception):
    """
    A Python package uses an unsupported build method
    """

    def __init__(self, name: str, version: str):
        super().__init__(f'Unsupported Python package {name}-{version}')
        self._message = f'Unsupported Python package {name}-{version}'
        self._name = name
        self._version = version

    @property
    def message(self) -> str:
        return self._message

    @property
    def name(self) -> str:
        return self._name

    @property
    def version(self) -> str:
        return self._version
