"""Parser for POL files."""
# gpoanalyzer/parse/pol_files.py

import os


class POLParser:
    """Class to parse Registry.pol files and extract relevant data."""

    def __init__(self) -> None:
        self.field_index = 0
        self.pol_str_tmp = ""
        self.data_size = 0
        self.current_row = {}
        self.results = {}
        self.pol_file = ""
        self.hive = ""

    def determine_hive(self):
        """Determine the hive type based on the file path."""
        if "User" in self.pol_file:
            return "HKCU"
        if "Machine" in self.pol_file:
            return "HKLM"
        return "?"

    def normalize(self, data):
        """Remove entries with null values from data."""
        return {key: value for key, value in data.items(
        ) if value["Type"] not in ["REG_NONE", "REG_BINARY"] and '??' not in value["Data"]}

    def parse_pol_file(self):
        """Parse a single POL file and extract relevant data."""
        pol_reg_types = ("REG_NONE", "REG_SZ", "REG_EXPAND_SZ", "REG_BINARY",
                         "REG_DWORD", "REG_DWORD_BIG_ENDIAN", "REG_LINK",
                         "REG_MULTI_SZ", "REG_RESOURCE_LIST", "REG_FULL_RESOURCE_DESCRIPTOR",
                         "REG_RESOURCE_REQUIREMENTS_LIST", "REG_QWORD")
        pol_blob_size = 1024

        if self.pol_file and os.path.exists(self.pol_file):
            with open(self.pol_file, 'rb') as file:
                pol_bytes = file.read()

                # Determine Hive
                self.hive = self.determine_hive()

                pol_bytes = pol_bytes[8:]

                index = 0
                self.current_row = {'name': self.pol_file, 'Hive': self.hive,
                                    'Key': '??', 'Value': '??', 'Type': '??', 'Data': '??'}
                self.field_index = 0
                self.pol_str_tmp = ""
                self.data_size = 0
                while index < len(pol_bytes):
                    if self.field_index == 0:  # key field
                        index = self.parse_key_field(pol_bytes, index)
                    elif self.field_index == 1:  # value field
                        index = self.parse_value_field(pol_bytes, index)
                    elif self.field_index == 2:  # type field
                        index = self.parse_type_field(
                            pol_bytes, index, pol_reg_types)
                    elif self.field_index == 3:  # size field
                        index = self.parse_size_field(pol_bytes, index)
                    elif self.field_index == 4:  # data field
                        index = self.parse_data_field(
                            pol_bytes, index, pol_blob_size)
                    else:
                        break

        return self.results

    def parse_key_field(self, pol_bytes, index):
        """Parse the key field in POL file."""
        if pol_bytes[index:index+4] == b'\x00\x00;\x00':
            if "[" in self.pol_str_tmp:
                self.pol_str_tmp = self.pol_str_tmp.replace(
                    "]", "").replace("[", "")
            self.current_row['Key'] = self.pol_str_tmp
            self.pol_str_tmp = ""
            self.field_index = 1
            index += 2
        else:
            self.pol_str_tmp += pol_bytes[index:index+2].decode('utf-16le')
            index += 2
        return index

    def parse_value_field(self, pol_bytes, index):
        """Parse the value field in POL file."""
        if pol_bytes[index:index+2] == b'\x00\x00':
            if "**del." in self.pol_str_tmp[1:]:
                self.pol_str_tmp = self.pol_str_tmp.replace("**del.", "")
            self.current_row['Value'] = self.pol_str_tmp[1:]
            self.pol_str_tmp = ""
            self.field_index = 2
            index += 2
        else:
            self.pol_str_tmp += pol_bytes[index:index+2].decode('utf-16le')
            index += 2
        return index

    def parse_type_field(self, pol_bytes, index, pol_reg_types):
        """Parse the type field in POL file."""
        if pol_bytes[index+4:index+6] == b';\x00':
            type_code = int.from_bytes(pol_bytes[index:index+1], 'little')
            self.current_row['Type'] = pol_reg_types[type_code]
            self.field_index = 3
            index += 6
        else:
            index += 2
        return index

    def parse_size_field(self, pol_bytes, index):
        """Parse the size field in POL file."""
        if pol_bytes[index+4:index+6] == b';\x00':
            self.data_size = int.from_bytes(pol_bytes[index:index+4], 'little')
            self.field_index = 4
            index += 6
        return index

    def parse_data_field(self, pol_bytes, index, pol_blob_size):
        """Parse the data field in POL file."""
        data = pol_bytes[index:index+self.data_size]
        if self.data_size > pol_blob_size:
            self.current_row['Data'] = "(BLOB)"
        else:
            if self.current_row['Type'] in ["REG_MULTI_SZ", "REG_SZ", "REG_EXPAND_SZ"]:
                while data[-2:] == b'\x00\x00':
                    data = data[:-2]
                self.current_row['Data'] = data.decode('utf-16le')
            if self.current_row['Type'] == "REG_DWORD":
                self.current_row['Data'] = f"0x{data[::-1].hex()}"

        index += self.data_size
        hashable_data = tuple(
            [self.current_row["Key"], self.current_row["Value"], self.current_row["Data"]])
        element_hash = hash(hashable_data)
        self.results[element_hash] = self.current_row
        self.current_row = {'name': self.pol_file, 'Hive': self.hive, 'Key': '??',
                            'Value': '??', 'Type': '??', 'Data': '??'}
        self.field_index = 0
        return index

    def parse(self, file_paths: str) -> dict:
        """Parse Registry POL files and extract relevant data."""
        self.results = {}
        try:
            for pol_file in file_paths:
                self.pol_file = pol_file
                file_results = self.parse_pol_file()
                self.results.update(file_results)
            final_results = self.normalize(self.results)
        except OSError as e:
            print("Exception: an error occurred in POLParser:", e)

        return final_results
