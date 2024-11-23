# root2csv/trees.py

"""
Functions specific to processing TTree objects.
"""

import logging
from typing import Any, Dict, List, Tuple

import numpy as np
import uproot


def process_tree(tree: Any) -> Tuple[List[str], List[List[Any]]]:
    """
    Process a ROOT TTree object and prepare data for CSV output.

    Args:
        tree: The TTree object to process.

    Returns:
        A tuple containing:
            - headers: Column headers for the CSV file.
            - rows: Data rows for the CSV file.

    Raises:
        ValueError: If no supported branches are found or data inconsistency is detected.
    """
    logging.info(f"Available branches: {tree.keys()}")

    try:
        # Get all arrays with numpy backend
        arrays = tree.arrays(library="np")
        logging.info(f"Arrays read: {list(arrays.keys())}")

        # Get headers from the arrays
        headers = list(arrays.keys())
        if not headers:
            error_msg = "No branches found in the tree."
            logging.error(error_msg)
            raise ValueError(error_msg)

        # Convert arrays to rows
        first_array = arrays[headers[0]]
        n_rows = len(first_array)

        rows: List[List[Any]] = []
        for i in range(n_rows):
            row = [arrays[header][i] for header in headers]
            rows.append(row)

        return headers, rows

    except Exception as e:
        logging.error(f"Error reading tree data: {str(e)}")
        raise


def filter_branches(tree: Any) -> Dict[str, np.ndarray]:
    """
    Filter branches that are supported for CSV output.
    This function is kept for backwards compatibility but not used in the main process.

    Args:
        tree: The TTree object.

    Returns:
        Dictionary of branch names and arrays.
    """
    supported_branches: Dict[str, np.ndarray] = {}
    for branch_name in tree.keys():
        try:
            supported_branches[branch_name] = tree[branch_name].array(library="np")
        except Exception as e:
            logging.warning(f"Skipping branch '{branch_name}': {str(e)}")
    return supported_branches
