# log_config.py
import logging
import sys
import pkgutil
import warnings

def configure_logging(verbose: bool, trace: bool, quiet: bool):
    level = logging.WARNING
    if (quiet):
        level = logging.ERROR
    elif (trace):
        level = logging.DEBUG
    elif (verbose):
        level = logging.INFO
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.setLevel(level)
    logger.addHandler(console_handler)
