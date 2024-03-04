# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/flake/recipe/formatted_python_package_list.py

This file defines the FormattedPythonPackageList class.

Copyright (C) 2023-today rydnr's rydnr/python-nix-flake-generator

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from .formatted_python_package import FormattedPythonPackage
from pythoneda.shared import Formatting
from typing import Callable, List


class FormattedPythonPackageList(Formatting):
    """
    Augments a list of PythonPackages to include formatting logic required by recipe templates.
    """

    def __init__(
        self,
        lst: List[FormattedPythonPackage],
        f: str = "__str__",
        indent: str = "",
        separator: str = "",
        initialPrefix: str = "",
        finalSuffix: str = "",
    ):
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

    def with_function(self, value: str):  # -> FormattedPythonPackageList:
        return FormattedPythonPackageList(
            self.list,
            value,
            self._indent,
            self._separator,
            self._initial_prefix,
            self._final_suffix,
        )

    def with_indentation(self, value: str):  # -> FormattedPythonPackageList:
        return FormattedPythonPackageList(
            self.list,
            self._func_name,
            value,
            self._separator,
            self._initial_prefix,
            self._final_suffix,
        )

    def with_separator(self, value: str):  # -> FormattedPythonPackageList:
        return FormattedPythonPackageList(
            self.list,
            self._func_name,
            self._indent,
            value,
            self._initial_prefix,
            self._final_suffix,
        )

    def with_initial_prefix(self, value: str):  # -> FormattedPythonPackageList:
        return FormattedPythonPackageList(
            self.list,
            self._func_name,
            self._indent,
            self._separator,
            value,
            self._final_suffix,
        )

    def with_final_suffix(self, value: str):  # -> FormattedPythonPackageList:
        return FormattedPythonPackageList(
            self.list,
            self._func_name,
            self._indent,
            self._separator,
            self._initial_prefix,
            value,
        )

    def _invoke_func(self, dep: FormattedPythonPackage):  # -> str:
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


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
