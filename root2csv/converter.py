# root2csv/converter.py

"""
Core functionality for converting ROOT objects to CSV files.
"""

from typing import Any, List, Tuple, Dict, cast
import logging
import numpy as np
import uproot
from .trees import process_tree
from .graphs import process_tgraph, process_tgrapherrors
from .utils import write_csv


def convert(input_file: str, output_file: str, object_path: str) -> None:
    """
    Convert a ROOT object to CSV format.

    Args:
        input_file: Path to the input ROOT file
        output_file: Path to the output CSV file
        object_path: Path to the object within the ROOT file

    Raises:
        ValueError: If the object is not found or has an unsupported type
        IOError: If there are file access issues
    """
    logging.info("Opening ROOT file...")
    try:
        root_file = uproot.open(input_file)
    except Exception as e:
        logging.error(f"Failed to open ROOT file '{input_file}': {e}")
        raise

    try:
        obj = get_object(root_file, object_path)
    except KeyError as e:
        logging.error(str(e))
        raise

    if obj is None:
        error_msg = f"Object '{object_path}' not found in file '{input_file}'."
        logging.error(error_msg)
        raise ValueError(error_msg)

    try:
        # Get object information
        logging.info(f"Object type: {type(obj)}")
        logging.info(f"Object keys: {obj.keys()}")

        # Check for specific branch patterns to identify graph-like structures
        branches = set(obj.keys())

        if {"fX", "fY", "fEX", "fEY"}.issubset(branches):
            logging.info(f"Processing as TGraphErrors '{object_path}'...")
            headers = ["x", "y", "ex", "ey"]
            arrays = obj.arrays(library="np")
            # Convert arrays to list of lists with float values
            rows: List[List[float]] = [
                list(map(float, [x, y, ex, ey]))
                for x, y, ex, ey in zip(arrays["fX"], arrays["fY"], arrays["fEX"], arrays["fEY"])
            ]
        elif {"fX", "fY"}.issubset(branches):
            logging.info(f"Processing as TGraph '{object_path}'...")
            headers = ["x", "y"]
            arrays = obj.arrays(library="np")
            # Convert arrays to list of lists with float values
            rows = [list(map(float, [x, y])) for x, y in zip(arrays["fX"], arrays["fY"])]
        else:
            logging.info(f"Processing as TTree '{object_path}'...")
            headers, rows = process_tree(obj)

        write_csv(output_file, headers, rows, input_file)

    except Exception as e:
        logging.error(f"Error processing object '{object_path}': {e}")
        raise

    logging.info("CSV file created successfully.")


def get_object(root_file: Any, object_path: str) -> Any:
    """
    Retrieve an object from the ROOT file, supporting nested directories.

    Args:
        root_file: The opened ROOT file
        object_path: Path to the object, e.g., 'dir1/dir2/tree'

    Returns:
        The requested object if found

    Raises:
        KeyError: If the object is not found in the ROOT file
    """
    current = root_file
    for part in object_path.strip("/").split("/"):
        try:
            current = current[part]
        except KeyError:
            error_msg = f"Object '{object_path}' not found in the ROOT file."
            logging.error(error_msg)
            raise KeyError(error_msg)
    return current


def list_objects(root_file: Any) -> List[Tuple[str, str]]:
    """
    List all Trees and Graphs in the ROOT file, including those in subdirectories.

    Args:
        root_file: The opened ROOT file

    Returns:
        List of tuples containing (object_path, classname)
    """
    objects: List[Tuple[str, str]] = []

    def recurse_keys(directory: Any, prefix: str = "") -> None:
        for name, obj in directory.items():
            try:
                full_path = f"{prefix}/{name}" if prefix else name

                # Check if it's a tree-like object
                if hasattr(obj, "keys"):
                    branches = set(obj.keys())
                    if {"fX", "fY", "fEX", "fEY"}.issubset(branches):
                        objects.append((full_path, "TGraphErrors"))
                    elif {"fX", "fY"}.issubset(branches):
                        objects.append((full_path, "TGraph"))
                    else:
                        objects.append((full_path, "TTree"))

                elif isinstance(obj, uproot.reading.ReadOnlyDirectory):
                    recurse_keys(obj, full_path)
            except Exception as e:
                logging.warning(f"Skipping object {name}: {e}")

    recurse_keys(root_file)
    return objects
