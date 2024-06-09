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

```bash
python -m gpoanalyzer <gpopath> [options]
```

```powershell
gpoanalyzer.exe <gpopath> [options]
```

### Mandatory Argument

- `gpopath`: Specifies the path to the GPO data directory.

### Module Options

- `--json/-jq`: Get data in JSON format. (Must be used with exactly one file argument.).
- `--find/-f TERM`: Search string or pattern on database data.

### General Options

- `--output FILE`: Outputs the result to a specified file.

### Analyzer Options

- `-registrypol`: Parse registry settings from Registry.pol files.
- `-shortcuts`: Retrieve shortcut configurations from XML files.
- `-scheduledtasks`: Analyze Scheduled Tasks from XML files.
- `-drives`: Extract network drive mappings from XML files.
- `-groups`: Analyze group membership settings from XML files.
- `-printers`: Retrieve printer configurations from Printers.xml..
- `-registryxml`: Parse settings from Registry.xml files.
- `-environmentvariables`: Retrieve environment variable settings from EnvironmentVariables.xml.
- `-files`: Extract file policies from Files.xml.
- `-services`: Analyze service configurations from Services.xml.
- `-folders`: Analyze folder redirection settings from Folder.xml.
- `-internetsettings`: Analyze settings from internet settings XML files.
- `-gpttmpl`: Extract Group Policy Template data, including Password and Kerberos policies.

# Examples

### Find Module

Search for a string in all parsed data

```bash
λ python -m gpoanalyzer "<GPO_FILES_PATH>" --find "AdmPwd"

Results
└── ('registrypol', -3475148589812524019)
    ├── name: <GPO_FILES_PATH>\{4080B15B-A69C-452C-8E4E-14886CF1740D}\Machine\Registry.pol
    ├── Hive: HKLM
    ├── Key: Software\Policies\Microsoft Services\AdmPwd
    ├── Value: AdmPwdEnabled
    ├── Type: REG_DWORD
    ├── Data: 0x00000001
    └── -------------------------------------------------------------------------------------------
```

Search for a pattern in all parsed data

```bash
λ python -m gpoanalyzer "<GPO_FILES_PATH>" --find "^(\\)(\\[\w\.-_]+){2,}(\\?)$"
```

### Report Module

Output all data to a file

```bash
λ python -m gpoanalyzer "<GPO_FILES_PATH>" --shortcuts --drives --folders --scheduledtasks -o output.txt
```

Output registry data to a file in json format:

```bash
λ python -m gpoanalyzer "<GPO_FILES_PATH>" --registrypol --json -o registry.pol.json
```

### JSON Module

Export `targetPath` value from shortcuts XML files configuration with `jq`

```bash
λ python -m gpoanalyzer "<GPO_FILES_PATH>" --shortcuts --json | jq '[.. | objects | select(has("targetPath")) | .targetPath]' | sort -u

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
