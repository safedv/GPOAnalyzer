"""This module provides the GPOAnalyzer CLI."""
# gpoanalyzer/cli.py

import argparse
import json
import os
import sys
from rich.console import Console

from gpoanalyzer.gpo_value_paths import gpo_value_paths
from gpoanalyzer.gpoanalyzer import FILENAMES, GPOAnalyzer
from gpoanalyzer.common import json_to_file, print_dict_as_tree

console = Console()


def parse_cmdline() -> argparse.ArgumentParser:
    """Parse command line arguments for GPO Analyzer."""
    parser = argparse.ArgumentParser(description=(
        "GPO Analyzer parses and enumerates Domain Group Policy Object (GPO) files."))

    # General arguments group
    general_args = parser.add_argument_group('General Options')
    general_args.add_argument(
        'gpopath', type=str, help='The path to the GPO data directory.')

    # Add mutually exclusive group for scan and json options
    exclusive_group = general_args.add_mutually_exclusive_group()
    exclusive_group.add_argument("--json", '-jq', action="store_true", help=(
        'Get data in JSON format. (Must be used with exactly one file argument.)'))
    exclusive_group.add_argument(
        "--find", '-f', type=str, help='Find string on all database tables.')
    general_args.add_argument(
        '--output', '-o', type=str, help='Output to a file. Specify the file path.')

    # Add file options
    files_args = parser.add_argument_group('Supported Files')

    files_args.add_argument('--shortcuts', action='store_true',
                            help='Retrieve data about configured shortcuts from XML files.')
    files_args.add_argument('--scheduledtasks', action='store_true',
                            help='Parse Scheduled Tasks from XML configurations.')
    files_args.add_argument('--drives', action='store_true',
                            help='Extract mappings of network drives from XML files.')
    files_args.add_argument('--groups', action='store_true',
                            help='Get group membership settings from XML configurations.')
    files_args.add_argument('--printers', action='store_true',
                            help='Retrieve printer configurations from Printers.xml.')
    files_args.add_argument(
        '--registryxml', action='store_true', help='Parse settings from Registry.xml.')
    files_args.add_argument('--environmentvariables', action='store_true',
                            help='Retrieve env variable settings from EnvironmentVariables.xml.')
    files_args.add_argument('--files', action='store_true',
                            help='Extract file policies from Files.xml.')
    files_args.add_argument('--services', action='store_true',
                            help='Get service configuration data from Services.xml.')
    files_args.add_argument('--folders', action='store_true',
                            help='Parse folder redirection settings from Folder.xml.')
    files_args.add_argument('--internetsettings', action='store_true',
                            help='Parse settings from Internet Explorer XML configurations.')
    files_args.add_argument('--registrypol', action='store_true',
                            help='Extract registry policies from Registry.pol.')
    files_args.add_argument('--gpttmpl', action='store_true',
                            help='Get Group Policy Template data')

    if len(sys.argv) == 2:
        parser.print_help()
        sys.exit(1)

    return parser


def print_as_tree(data):
    """Print data as tree to standard output"""
    for key in data:
        print_dict_as_tree(d={key: data[key]}, root_name="Results")


def app():
    """Main function of the CLI interface."""

    # Parse the command line arguments
    parser = parse_cmdline()
    args = parser.parse_args()

    # Check if the provided GPO file path exists
    if not os.path.exists(args.gpopath):
        console.print(
            f"[red]Error: The GPO file path '{args.gpopath}' does not exist.[/red]")
        return

    # Initialize the GPOAnalyzer with the provided GPO file path
    gpoanalyzer = GPOAnalyzer(gpo_file_path=args.gpopath)

    # Collect the file arguments based on the provided command line arguments
    file_args = [
        file_key for file_key in gpo_value_paths if getattr(args, file_key)]

    if args.find:
        # If the find argument is provided, parse the necessary files
        if len(file_args) == 0:
            parsed_data = gpoanalyzer.parse(FILENAMES)
        else:
            parsed_data = gpoanalyzer.parse(file_args)

        # Search the parsed data for the search term
        find_result = gpoanalyzer.find(data=parsed_data, search_term=args.find)

        # Print the search results as a tree structure
        if find_result:
            print_as_tree(find_result)
        else:
            console.print(
                "[yellow]No results found for the given search term.[/yellow]")
    else:
        # Parse the necessary files
        parsed_data = gpoanalyzer.parse(file_args)

        # Check if parsed_data is empty and print a message if so
        if not parsed_data:
            console.print("[red]No data found.[/red]")
            return

        # If output argument is provided, save the parsed data to a file
        if args.output:
            if json_to_file(args.output, parsed_data):
                console.print(
                    f"[green]File created successfully at: '{args.output}'[/green]")
            return

        # Print the parsed data in JSON format or as a tree structure
        if args.json:
            console.print(json.dumps(parsed_data, indent=2))
        else:
            print_as_tree(parsed_data)
