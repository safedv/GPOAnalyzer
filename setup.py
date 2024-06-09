"""Setup script for the GPOAnalyzer package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="gpoanalyzer",
    version="0.1.0",
    author="Davide Valitutti (@safedv)",
    author_email="davidevalitutti@pm.me",
    description="Tool for offline analysis of Group Policy Objects (GPO)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/safedv/GPOAnalyzer",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
