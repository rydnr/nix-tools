from domain.flake.flake import Flake
from domain.formatting import Formatting
from domain.flake.license import License

class FormattedFlake(Formatting):
    """
    Augments Flake class to include formatting logic required by recipe templates.
    """
    def __init__(self, flk: Flake):
        """Creates a new instance"""
        super().__init__(flk)

    @property
    def flake(self) -> Flake:
        return self._fmt

    def version_with_underscores(self):
        return self.flake.version.replace(".", "_")

    def description(self):
        return self.flake.python_package.info["description"]

    def license(self):
        return License.from_pypi(self.flake.python_package.info.get("license", "")).nix

    def sha256(self):
        return self.flake.python_package.release.get("hash", "")

    def repo_url(self):
        result = ""
        if self.flake.python_package.git_repo:
            result = self.flake.python_package.git_repo.url
        return result

    def repo_rev(self):
        result = ""
        if self.flake.python_package.git_repo:
            result = self.flake.python_package.git_repo.rev
        return result

    def repo_owner(self):
        result = ""
        if self.flake.python_package.git_repo:
            result, _ = self.flake.python_package.git_repo.repo_owner_and_repo_name()
        return result

    def repo_name(self):
        result = ""
        if self.flake.python_package.git_repo:
            _, result = self.flake.python_package.git_repo.repo_owner_and_repo_name()
        return result
