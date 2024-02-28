from typing import List


class RequirementstxtUtils:
    """
    Utilities for dealing with requirements.txt or dev_requirements.txt files
    """

    @classmethod
    def read_requirements_txt(cls, gitRepo) -> List:
        return cls._read_requirements_txt("requirements.txt", gitRepo)

    @classmethod
    def read_dev_requirements_txt(cls, gitRepo) -> List:
        return cls._read_requirements_txt("dev_requirements.txt", gitRepo)

    @classmethod
    def _read_requirements_txt(cls, fileName: str, gitRepo) -> List:
        result = {}
        if gitRepo:
            contents = gitRepo.get_file(fileName)
            if contents:
                result = cls.parse_requirements_txt(contents)
        return result

    @classmethod
    def parse_requirements_txt(cls, contents: str) -> List:
        lines = contents.splitlines()
        # Filter out comments and blank lines
        packages = [line.strip() for line in lines if line.strip() and not line.startswith('#') and not line.startswith('-e ')]
        return packages
