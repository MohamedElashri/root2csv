# root2csv/logging_config.py

"""
Configure logging for the root2csv package.
"""

import logging


def configure_logging() -> None:
    """Configure the logging settings for the package."""
    logging.basicConfig(level=logging.INFO, format="root2csv: %(levelname)s: %(message)s")
