"""Parser for INF files."""
# gpoanalyzer/parse/inf_files.py

import re


class INFParser:
    """Class to parse GtpTmpl.inf files and extract relevant data."""

    def __init__(self) -> None:
        self.results = {}
        # Regular expressions to identify sections and key/value pairs
        self.section_pattern = re.compile(r"\[\s*(.*?)\s*\]")
        self.key_value_pattern = re.compile(r"(\S+)\s*=\s*(.*)")

    def read_file(self, file):
        """Read an INF file and populate the results dictionary with its contents."""
        current_section = None

        with open(file, 'r', encoding='utf-16') as f:
            for line in f:
                line = line.strip()
                # Ignore empty lines or comments
                if not line or line.startswith(';'):
                    continue

                # Check if the line is a section
                section_match = self.section_pattern.match(line)
                if section_match:
                    # Extract the section name
                    current_section = section_match.group(1)
                    if current_section not in self.results:
                        self.results[current_section] = {}

                else:
                    # Otherwise, it should be a key/value pair
                    key_value_match = self.key_value_pattern.match(line)
                    if key_value_match:
                        key, value = key_value_match.groups()
                        self.results[current_section][key] = value

    def parse(self, file_paths: str) -> dict:
        """Parse GtpTmpl.inf files and extract relevant data."""
        try:
            for file in file_paths:
                self.read_file(file)
        except OSError as e:
            print("Exception: an error occur in INFParser:", e)

        return self.results
