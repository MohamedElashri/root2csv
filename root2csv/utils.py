# root2csv/utils.py

"""
Utility functions for the root2csv package.
"""

import csv
import logging
from typing import Any, List


def write_csv(
    output_path: str, headers: List[str], rows: List[List[Any]], root_file_name: str
) -> None:
    """
    Write data to a CSV file.

    Parameters:
        output_path: Path to the output CSV file.
        headers: Column headers.
        rows: Data rows.
        root_file_name: Name of the input ROOT file.

    Raises:
        IOError: If the CSV file cannot be written.
    """
    try:
        with open(output_path, "w", newline="") as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=";")
            csv_writer.writerow([f"## Automatically generated from '{root_file_name}'"])
            csv_writer.writerow(headers)
            for row in rows:
                csv_writer.writerow(row)
        logging.info(f"CSV file '{output_path}' written successfully.")
    except IOError as e:
        error_msg = f"Failed to write CSV file '{output_path}': {e}"
        logging.error(error_msg)
        raise
