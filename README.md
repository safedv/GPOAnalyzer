# GPOAnalyzer

![Python](https://img.shields.io/badge/python-v3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**GPOAnalyzer** is a tool designed for penetration testers and red teamers to assist in the analysis of domain Group Policy Objects (GPO) files, located in the SYSVOL directory.

GPOAnalyzer is valuable for quickly identifying critical information such as domain configuration, registry keys, policies, web targets, network shares, and more. Additionally, it provides easily interpretable outputs and supports data exportation in JSON format for seamless integration with complementary tools like `jq`.

# Installation

### Executable

Download the executable from [release page](https://github.com/safedv/GPOAnalyzer/releases).

### Python Module

Alternatively, you can install **GPOAnalyzer**, you need `Python 3.6` or higher. Clone the repository and install the required dependencies:

```bash
git clone https://github.com/safedv/GPOAnalyzer.git
cd GPOAnalyzer
pip install .
```

# Usage

Run the tool from the command line using the following syntax:

#### Linux

```bash
python -m gpoanalyzer --help
```

#### Windows

```powershell
gpoanalyzer.exe --help
```

#### Output

```
usage: python -m gpoanalyzer [-h] [--json | --find FIND] [--output OUTPUT] [--shortcuts] [--scheduledtasks] [--drives] [--groups] [--printers] [--registryxml] [--envvars] [--files] [--services]
                             [--folders] [--internetsettings] [--registrypol] [--gpttmpl]
                             gpopath

GPO Analyzer parses and enumerates Domain Group Policy Object (GPO) files.

options:
  -h, --help            show this help message and exit

General Options:
  gpopath               Path to the GPO data directory
  --json, -jq           Output data in JSON format
  --find FIND, -f FIND  Search for a specific string or pattern
  --output OUTPUT, -o OUTPUT
                        Output results to a specified file path

Supported Files:
  --shortcuts           Extract shortcut configurations from Shortcuts XML files
  --scheduledtasks      Extract scheduled tasks from ScheduledTasks XML files
  --drives              Extract network drive mappings from Drives XML files
  --groups              Extract group membership settings from Groups XML files
  --printers            Extract printer configurations from Printers.xml
  --registryxml         Extract settings from Registry.xml
  --envvars             Extract env variable settings from EnvironmentVariables.xml
  --files               Extract file policies from Files.xml
  --services            Extract service configurations from Services.xml
  --folders             Extract folder settings from Folders.xml
  --internetsettings    Extract internet settings from InternetSettings XML files
  --registrypol         Extract registry settings from Registry.pol
  --gpttmpl             Extract group policy template data from GptTmpl.inf files
```

# Examples

### Find Module

Search for a string in all parsed data

```bash
python -m gpoanalyzer "<GPO_FILES_PATH>" --find "AdmPwd"
```

Search for a pattern in all parsed data

```bash
python -m gpoanalyzer "<GPO_FILES_PATH>" --find "^(\\)(\\[\w\.-_]+){2,}(\\?)$"
```

### Report Module

Output all data to a file

```bash
python -m gpoanalyzer "<GPO_FILES_PATH>" --shortcuts --drives --folders --scheduledtasks -o output.txt
```

Output registry data to a file in json format:

```bash
python -m gpoanalyzer "<GPO_FILES_PATH>" --registrypol --json -o registry.pol.json
```

### JSON Module

Export `targetPath` value from shortcuts XML files configuration with `jq`

```bash
python -m gpoanalyzer "<GPO_FILES_PATH>" --shortcuts --json | jq '[.. | objects | select(has("targetPath")) | .targetPath]' | sort -u
```

#### Output

```
"http://example1.com"
"https://example2.com"
"http://example3.com"
"10.10.12.120"
"\\SHARE\\LOL"
```

# Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your improvements.

# License

GPOAnalyzer is released under the MIT License. See `LICENSE` file for details.
