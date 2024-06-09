"""Common utility functions and classes."""
# gpoanalyzer/common.py

import json
import os
from rich.tree import Tree
from rich.console import Console


def list_files(gpo_path: str, target_filename: str):
    """List files in the given path that match the target filename.

    Args:
        gpo_path (str): The path to search for files.
        target_filename (str): The filename to search for.
    """
    files_info = []

    try:
        for root, _, files in os.walk(gpo_path):
            for file in files:
                try:
                    if file.lower() == target_filename.lower():
                        full_path = os.path.join(root, file)
                        size = os.path.getsize(full_path)
                        files_info.append((full_path, size, file))
                except OSError:
                    continue
    except OSError as e:
        print("An error occurred while listing files:", e)

    if not files_info:
        return None

    # Sort by size in descending order
    files_info.sort(key=lambda x: x[1], reverse=True)

    result_data = [x[0] for x in files_info]
    return result_data


def json_to_file(filepath, data):
    """Write data to a json file at the specified filepath."""
    try:
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(json.dumps(data))
            return True
    except OSError as e:
        print("An exception occurred while writing json file:", e)

    return False


def extract_data_from_list(json_list, config):
    """
    Extracts data from a list of JSON objects based on a configuration.

    :param json_list: The list of JSON objects to extract data from.
    :param config: A dictionary specifying the keys and paths to extract.
    :return: A list of dictionaries with the extracted data.
    """
    extracted_data_list = []

    for json_obj in json_list:
        extracted_data = {}
        for key, path in config.items():
            try:
                # Navigate the JSON to reach the desired value
                value = navigate_path(json_obj, path.split('.'))
                extracted_data[key] = value
            except (KeyError, IndexError, TypeError):
                # Handle missing keys or invalid paths
                extracted_data[key] = None
        extracted_data_list.append(extracted_data)

    return extracted_data_list


def navigate_path(json_obj, path_parts):
    """
    Navigates through a JSON object following the specified path.

    :param json_obj: The JSON object to extract data from.
    :param path_parts: A list of parts of the path to follow.
    :return: The value found at the end of the path.
    """
    for part in path_parts:
        if isinstance(json_obj, list):
            part = int(part)
        try:
            json_obj = json_obj[part]
        except (KeyError, IndexError, TypeError):
            return None
    return json_obj


def extract_data(json_obj, config):
    """
    Extracts data from a JSON object based on a configuration,
    considering both lists and dictionaries.

    :param json_obj: The JSON object to extract data from.
    :param config: A dictionary specifying the keys and paths to extract.
    :return: A dictionary with extracted data for each key.
    """
    all_extracted_data = {}

    def extract_single_object(data, config):
        extracted_data = {}
        for key, path in config.items():
            try:
                value = navigate_path(data, path.split('.'))
                if value:
                    extracted_data[key] = value
            except (KeyError, IndexError, TypeError):
                continue
        return extracted_data

    for key, value in json_obj.items():
        if isinstance(value, list):
            extracted_data = extract_data_from_list(value, config)
            all_extracted_data[key] = extracted_data
        elif isinstance(value, dict):
            extracted_data = extract_single_object(value, config)
            all_extracted_data[key] = extracted_data
        else:
            if value:
                all_extracted_data[key] = value

    return all_extracted_data


def print_dict_as_tree(d, root_name="ROOT"):
    """
    Print a nested dictionary as a tree structure using the `rich` library.

    This function takes a nested dictionary and prints it as a tree structure,
    making it easier to visualize the hierarchy and relationships between the data.
    Each key-value pair is represented as a branch of the tree, and lists are handled
    by creating sub-branches for each item in the list.

    Args:
        d (dict): The nested dictionary to be printed.
        root_name (str): The name of the root node of the tree. Defaults to "ROOT".
    """
    # Initialize a Console object from the `rich` library
    console = Console()

    # Create the root of the tree with the given root name, styled in bold magenta
    tree = Tree(f"[bold magenta]{root_name}[/bold magenta]")

    def add_branch(branch, tree):
        """
        Recursively add branches to the tree.

        This helper function adds branches to the tree for each key-value pair in the dictionary.
        If the value is a dictionary, it creates a subtree and recursively adds branches.
        If the value is a list, it creates a subtree for each item in the list.
        If the value is a simple data type, it adds it as a leaf node.

        Args:
            branch (dict): The current dictionary to add as a branch.
            tree (Tree): The current tree node to add branches to.
        """
        for idx, (key, value) in enumerate(branch.items(), start=1):
            # If the value is a dictionary, create a subtree and recursively add branches
            if isinstance(value, dict):
                sub_tree = tree.add(f"[bold blue]{key}[/bold blue]")
                add_branch(value, sub_tree)
            elif isinstance(value, list):
                # Create a subtree for the list (currently not using key in the node)
                list_tree = tree.add("")
                for i, item in enumerate(value):
                    # Create a subtree for each item in the list
                    item_tree = list_tree.add(
                        f"[bold blue]GPO Path[/bold blue]: [bold yellow]{key}")
                    if isinstance(item, dict):
                        # If the item is a dictionary, recursively add branches
                        add_branch(item, item_tree)
                    elif isinstance(item, list):
                        # If the item is a list, recursively add branches for each sub-item
                        for item2 in item:
                            add_branch(item2, item_tree)
                    else:
                        # If the item is a simple data type, add it as a leaf node
                        item_tree.add(f"[bold cyan]{item}[/bold cyan]")

                    if i < len(value) - 1:
                        # Add a blank line between items in the list for readability
                        tree.add("")
            else:
                # If the value is a simple data type, add it as a leaf node
                tree.add(
                    f"[bold blue]{key}[/bold blue]: [bold cyan]{value}[/bold cyan]")

                # Add a separator line between elements if it's the last element in the branch
                if idx == len(branch):
                    tree.add(f"{'-' * 100}")

    # Add the branches to the root tree
    add_branch(d, tree)

    # Print the tree to the console
    console.print(tree)
