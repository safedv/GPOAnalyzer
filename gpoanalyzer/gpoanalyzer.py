"""Main module for GPOAnalyzer."""
# gpoanalyzer/gpoanalyzer.py

import os
import re
from gpoanalyzer.parse.inf_files import INFParser
from gpoanalyzer.parse.pol_files import POLParser
from gpoanalyzer.parse.xml_files import XMLParser
from gpoanalyzer.gpo_value_paths import gpo_value_paths

from gpoanalyzer.common import (
    list_files,
    extract_data,
)

FILENAMES = {
    "shortcuts": "shortcuts.xml",
    "scheduledtasks": "scheduledtasks.xml",
    "drives": "drives.xml",
    "groups": "groups.xml",
    "printers": "printers.xml",
    "registryxml": "registry.xml",
    "envvars": "environmentvariables.xml",
    "files": "files.xml",
    "services": "services.xml",
    "folders": "folders.xml",
    "internetsettings": "internetsettings.xml",
    "registrypol": "registry.pol",
    "gpttmpl": "gpttmpl.inf",
}


def get_parser(parser_type):
    """
    A factory method for creating parser instances based on the file type.

    This method provides a method to create different types of parsers
    depending on the file extension provided. It supports parsers for XML, POL,
    and INF file types.

    Supported file types:
        - .xml: Uses `XMLParser`
        - .pol: Uses `POLParser`
        - .inf: Uses `INFParser`

    Example usage:
        parser = ParserFactory(".xml")
        parser.parse("path/to/file.xml")
    """
    parsers = {
        ".xml": XMLParser,
        ".pol": POLParser,
        ".inf": INFParser,
    }
    parser_class = parsers.get(parser_type)
    if parser_class:
        return parser_class()
    raise ValueError("Invalid parser type: No parser found!")


class GPOAnalyzer:
    """Class for analyzing Group Policy Objects (GPOs)."""

    def __init__(self, gpo_file_path: str) -> None:
        """Initialize the GPOAnalyzer instance.

        Args:
            gpo_file_path (str): The path to the GPO files.
        """
        self.gpo_file_path = gpo_file_path
        self.gpo_value_paths = gpo_value_paths

    def parse(self, user_args):
        """
        Parse the user-provided arguments and extract relevant data from files.

        This method processes a list of user arguments to extract and parse data
        from files specified in the configuration. It uses different parsers based
        on the file extensions and supports various argument types.

        Args:
            user_args (list): A list of arguments provided by the user indicating
                              which files to parse.

        Returns:
            dict: A dictionary containing the parsed and extracted data organized
                  by the user arguments and file paths.

        Notes:
            - If an argument in `user_args` is not in `self.gpo_value_paths`, it is skipped.
            - The method retrieves file paths using the `list_files` function and
              parses the files using the appropriate parser from `ParserFactory`.
            - The extracted data for each file is processed and organized in the
              `results` dictionary, with file paths as keys.
        """
        results = {}

        # Iterate over each user-provided argument
        for arg in user_args:
            # Skip arguments not present in the configuration
            if arg not in self.gpo_value_paths:
                continue

            # Retrieve the filename associated with the current argument
            filename = FILENAMES.get(arg)
            # Extract the file extension from the filename
            _, file_ext = os.path.splitext(filename)

            # Get the appropriate parser based on the file extension
            parser = get_parser(file_ext)

            # Retrieve file paths using the `list_files` function
            file_paths = list_files(
                gpo_path=self.gpo_file_path, target_filename=filename)

            # If no file paths are found, skip to the next argument
            if not file_paths:
                continue

            # Special case handling for specific argument types
            if arg in ["registrypol", "gpttmpl"]:
                results[arg] = parser.parse(file_paths)
                continue

            # Process each file path
            for file_path in file_paths:
                # Parse the file using the appropriate parser
                data = parser.parse(file_path)

                # If parsing fails or returns no data, skip to the next file
                if not data:
                    continue

                # Extract relevant data from the parsed file
                extracted_data = extract_data(
                    data, self.gpo_value_paths.get(arg))

                # Initialize the results dictionary for the argument if not already present
                if arg not in results:
                    results[arg] = {}

                # List comprehension to hold extracted values excluding the 'clsid' key
                tmp_list = [values for key,
                            values in extracted_data.items() if key != "clsid"]

                # If extracted data is found, add it to the results dictionary
                if tmp_list:
                    results[arg][file_path] = tmp_list

        return results

    def find(self, data, search_term: str):
        """
        Search for a string or regex pattern within a nested dictionary.

        Args:
            data (dict): The nested dictionary to search within.
            search_term (str or pattern): The string or regex pattern to search for.

        Returns:
            dict: A dictionary where the keys are the positions of the matched elements
                and the values are the corresponding sub-dictionaries 
                or sub-lists containing the match.
        """
        matches = {}

        # Compile the search pattern case insensitivity
        search_pattern = re.compile(search_term, re.IGNORECASE)

        def search_recursive(dictionary, path):
            for key, value in dictionary.items():
                current_path = path + [key]
                if isinstance(value, dict):
                    search_recursive(value, current_path)
                elif isinstance(value, list):
                    search_in_list(value, current_path)
                elif isinstance(value, str):
                    if search_pattern.search(value):
                        matches[tuple(path)] = dictionary

        def search_in_list(lst, path):
            for idx, item in enumerate(lst):
                current_path = path + [idx]
                if isinstance(item, dict):
                    search_recursive(item, current_path)
                elif isinstance(item, list):
                    search_in_list(item, current_path)
                elif isinstance(item, str):
                    if search_pattern.search(item):
                        matches[tuple(path)] = lst

        search_recursive(data, [])

        return matches
