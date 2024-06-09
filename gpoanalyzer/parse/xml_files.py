"""Parser for XML files."""
# gpoanalyzer/parse/xml_files.py

import xml.etree.ElementTree as ET


class XMLParser:
    """Class to parse XML files and extract relevant data."""

    def __init__(self) -> None:
        pass

    def to_dict(self, element):
        """Convert an XML element into a dictionary."""
        # Initialize the dictionary with the attributes of the element
        node = dict(element.attrib)

        # If the element has sub-elements, handle them recursively
        if element:
            # Handle cases where there are multiple sub-elements with the same tag
            children = {}
            for child in element:
                child_dict = self.to_dict(child)
                if child.tag in children:
                    # If the tag is already present and not a list, convert it to a list
                    if not isinstance(children[child.tag], list):
                        children[child.tag] = [children[child.tag]]
                    children[child.tag].append(child_dict)
                else:
                    children[child.tag] = child_dict
            node.update(children)
        # If the element has text, add that as a '_text' value
        elif element.text:
            text = element.text.strip()
            if text:
                node['_text'] = text

        return node

    def parse(self, file_path: str):
        """Read an XML file and convert it into a Python object."""
        tree = ET.parse(file_path)
        root = tree.getroot()
        return self.to_dict(root)
