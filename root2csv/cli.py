# root2csv/cli.py

"""
Command-line interface for the root2csv package.
"""

import argparse
import sys
import logging
from typing import NoReturn
import uproot
from .converter import convert, list_objects
from .logging_config import configure_logging


def main() -> None:
    """
    Main entry point for the command-line interface.
    Sets up argument parsing and executes the appropriate conversion functions.
    """
    parser = argparse.ArgumentParser(description="Convert ROOT Trees and Graphs to CSV files.")
    parser.add_argument("-f", "--file", required=True, help="Path to input ROOT file name")
    parser.add_argument("-o", "--output", default="output.csv", help="Path to output CSV file name")
    parser.add_argument(
        "-t", "--tree", default="tree", help="Name or path of the tree or graph to convert"
    )
    parser.add_argument(
        "-l", "--list", action="store_true", help="List available Trees and Graphs in the ROOT file"
    )
    args = parser.parse_args()

    configure_logging()

    try:
        root_file = uproot.open(args.file)

        if args.list:
            logging.info(f"Listing available Trees and Graphs in '{args.file}':")
            objects = list_objects(root_file)
            if not objects:
                logging.info("No Trees or Graphs found in the ROOT file.")
            else:
                for obj_path, classname in objects:
                    print(f" - {obj_path} ({classname})")
            sys.exit(0)

        convert(args.file, args.output, args.tree)
    except Exception as e:
        logging.error(str(e))
        sys.exit(1)
