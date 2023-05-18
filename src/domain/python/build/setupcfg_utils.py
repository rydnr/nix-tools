import configparser
from typing import Dict, List


class SetupcfgUtils():
    """
    Utilities for dealing with setup.cfg files
    """

    @classmethod
    def parse_setup_cfg(cls, contents: str) -> Dict:
        config = configparser.ConfigParser()
        config.read_string(contents)
        # Convert to a dictionary
        return {section: dict(config[section]) for section in config.sections()}

    @classmethod
    def read_setup_cfg(cls, gitRepo) -> Dict:
        result = {}
        if gitRepo:
            setupcfg_contents = gitRepo.get_file("setup.cfg")
            if setupcfg_contents:
                result = cls.parse_setup_cfg(setupcfg_contents)
        return result

