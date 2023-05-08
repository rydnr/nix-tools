from domain.recipe.formatted_python_package import FormattedPythonPackage

from typing import Callable, List

class FormattedPythonPackageList():
    """
    Augments a list of PythonPackages to include formatting logic required by recipe templates.
    """

    def __init__(self, lst: List[FormattedPythonPackage], f: str = "__str__", indent: str = "", separator: str = "", initialPrefix: str = "", finalSuffix: str = ""):
        """Creates a new instance"""
        self._list = lst
        self._func_name = f
        self._indent = indent
        self._separator = separator
        self._initial_prefix = initialPrefix
        self._final_suffix = finalSuffix

    @property
    def list(self) -> List[FormattedPythonPackage]:
        return self._list

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
        return FormattedPythonPackageList(self.list, value, self.indent, self.separator, self.initial_prefix, self.final_suffix)

    def with_indentation(self, value: str) :#-> FormattedPythonPackageList:
        return FormattedPythonPackageList(self.list, self.func_name, value, self.separator, self.initial_prefix, self.final_suffix)

    def with_separator(self, value: str) :#-> FormattedPythonPackageList:
        return FormattedPythonPackageList(self.list, self.func_name, self.indent, value, self.initial_prefix, self.final_suffix)

    def with_initial_prefix(self, value: str) :#-> FormattedPythonPackageList:
        return FormattedPythonPackageList(self.list, self.func_name, self.indent, self.separator, value, self.final_suffix)

    def with_final_suffix(self, value: str) :#-> FormattedPythonPackageList:
        return FormattedPythonPackageList(self.list, self.func_name, self.indent, self.separator, self.initial_prefix, value)

    def invoke_func(self, dep: FormattedPythonPackage):#-> str:
        func = getattr(dep, self.func_name)

        if callable(func):
            result = func()
            print(f'{dep}.{self.func_name}() -> {result}')
        else:
            result = func
            print(f'{dep}.{self.func_name} -> {result}')

        return result

    def __str__(self):

        return f'{self.initial_prefix}{self.separator.join([f"{self.indent}{self.invoke_func(dep)}" for dep in self.list])}{self.final_suffix}'

    def __getattr__(self, attr):
        """
        Delegate any method call to the wrapped instance.
        """
        return getattr(self._list, attr)
