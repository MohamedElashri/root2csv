# root2csv/graphs.py

"""
Functions specific to processing TGraph and TGraphErrors objects.
"""

from typing import Tuple, List, Any, cast
import numpy as np
import numpy.typing as npt
import logging


def process_tgraph(graph: Any) -> Tuple[List[str], List[List[float]]]:
    """
    Process a TGraph object and extract x and y data arrays.

    Args:
        graph: The TGraph object to process.

    Returns:
        A tuple containing:
            - headers: List of column names ['x', 'y']
            - rows: List of data rows [x, y]

    Raises:
        KeyError: If required data members are missing.
        ValueError: If data arrays have inconsistent lengths.
    """
    logging.info(f"Processing TGraph data structure: {dir(graph)}")

    try:
        # Try accessing data directly as dictionary
        data = graph.values()  # Get all the data
        logging.info(f"Available data keys: {list(data.keys())}")

        x = data["x"]
        y = data["y"]

        if len(x) != len(y):
            error_msg = "x and y arrays have different lengths in TGraph."
            logging.error(error_msg)
            raise ValueError(error_msg)

        headers = ["x", "y"]
        # Convert tuple to list and ensure float type
        rows = [list(map(float, row)) for row in zip(x, y)]
        return headers, rows

    except Exception as e:
        logging.error(f"Error processing TGraph: {e}")
        raise


def process_tgrapherrors(graph_errors: Any) -> Tuple[List[str], List[List[float]]]:
    """
    Process a TGraphErrors object and extract x, y, ex, and ey data arrays.

    Args:
        graph_errors: The TGraphErrors object to process.

    Returns:
        A tuple containing:
            - headers: List of column names ['x', 'y', 'ex', 'ey']
            - rows: List of data rows [x, y, ex, ey]

    Raises:
        KeyError: If required data members are missing.
        ValueError: If data arrays have inconsistent lengths.
    """
    logging.info(f"Processing TGraphErrors data structure: {dir(graph_errors)}")

    try:
        # Try accessing data directly as dictionary
        data = graph_errors.values()  # Get all the data
        logging.info(f"Available data keys: {list(data.keys())}")

        x = data["x"]
        y = data["y"]
        ex = data["ex"]
        ey = data["ey"]

        lengths = [len(x), len(y), len(ex), len(ey)]
        if len(set(lengths)) != 1:
            error_msg = "Data arrays have different lengths in TGraphErrors."
            logging.error(error_msg)
            raise ValueError(error_msg)

        headers = ["x", "y", "ex", "ey"]
        # Convert tuple to list and ensure float type
        rows = [list(map(float, row)) for row in zip(x, y, ex, ey)]
        return headers, rows

    except Exception as e:
        logging.error(f"Error processing TGraphErrors: {e}")
        raise
