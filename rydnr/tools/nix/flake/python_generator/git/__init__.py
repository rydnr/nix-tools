# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/git/__init__.py

This file ensures rydnr.tools.nix.flake.python_generator.git is a namespace.

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
__path__ = __import__("pkgutil").extend_path(__path__, __name__)

from .error_cloning_git_repository import ErrorCloningGitRepository
from .git_add_failed import GitAddFailed
from .git_checkout_failed import GitCheckoutFailed
from .git_init_failed import GitInitFailed
from .git_repo import GitRepo
from .git_repo_found import GitRepoFound
from .git_repo_repo import GitRepoRepo
from .git_repo_requested import GitRepoRequested
from .git_repo_resolver import GitRepoResolver

# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
