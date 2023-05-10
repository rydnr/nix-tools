from domain.formatting import Formatting
from domain.recipe.formatted_python_package import FormattedPythonPackage

from typing import Callable, List

class FormattedPythonPackageList(Formatting):
    """
    Augments a list of PythonPackages to include formatting logic required by recipe templates.
    """

    def __init__(self, lst: List[FormattedPythonPackage], f: str = "__str__", indent: str = "", separator: str = "", initialPrefix: str = "", finalSuffix: str = ""):
        """Creates a new instance"""
        super().__init__(lst)
        self._func_name = f
        self._indent = indent
        self._separator = separator
        self._initial_prefix = initialPrefix
        self._final_suffix = finalSuffix

    @property
    def list(self) -> List[FormattedPythonPackage]:
        return self._fmt

    @property
    def func_name(self) -> str:
        return self._func_name

    @property
    def indent(self) -> str:
        return self._indent

    @property
    def separator(self) -> str:
        return self._separator

    @property
    def initial_prefix(self) -> str:
        return self._initial_prefix

    @property
    def final_suffix(self) -> str:
        return self._final_suffix

    def with_function(self, value: str) :#-> FormattedPythonPackageList:
        return FormattedPythonPackageList(self.list, value, self._indent, self._separator, self._initial_prefix, self._final_suffix)

    def with_indentation(self, value: str) :#-> FormattedPythonPackageList:
        return FormattedPythonPackageList(self.list, self._func_name, value, self._separator, self._initial_prefix, self._final_suffix)

    def with_separator(self, value: str) :#-> FormattedPythonPackageList:
        return FormattedPythonPackageList(self.list, self._func_name, self._indent, value, self._initial_prefix, self._final_suffix)

    def with_initial_prefix(self, value: str) :#-> FormattedPythonPackageList:
        return FormattedPythonPackageList(self.list, self._func_name, self._indent, self._separator, value, self._final_suffix)

    def with_final_suffix(self, value: str) :#-> FormattedPythonPackageList:
        return FormattedPythonPackageList(self.list, self._func_name, self._indent, self._separator, self._initial_prefix, value)

    def _invoke_func(self, dep: FormattedPythonPackage): #-> str:
        result = ""

        func = getattr(dep, self.func_name)

        if callable(func):
            result = func()
        else:
            result = func

        return result

    def __str__(self):

        result = ""
        if len(self.list) > 0:
            result = f'{self.initial_prefix}{self.separator.join([f"{self.indent}{self._invoke_func(dep)}" for dep in self.list])}{self.final_suffix}'

        return result

    def __getattr__(self, attr):
        """
        Delegate any method call to the wrapped instance.
        """
        return getattr(self.list, attr)
