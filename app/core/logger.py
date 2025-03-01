"""
Customised App logger
"""

import logging
import sys

def configure_logging(level="INFO", log_file="app.log"):
    """Configures the global logging settings."""
    logger = logging.getLogger()
    logger.setLevel(level)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # File handler
    fh = logging.FileHandler(log_file)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger


logger = configure_logging("DEBUG")
