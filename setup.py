#!/usr/bin/env python
"""
Setup file for the ActiveTrail SDK package.
"""

import os
from setuptools import setup, find_packages

# Read the contents of the README file
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

# Read the requirements from requirements.txt
with open("requirements.txt", encoding="utf-8") as f:
    install_requires = [line.strip() for line in f if line.strip()]

# Package version
version = "0.2.0"  # Updated for the refactored version

setup(
    name="activetrail-sdk",
    version=version,
    description="Python SDK for the ActiveTrail API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Elior Cohen",
    author_email="eliorc1988@gmail.com",
    url="https://github.com/Eliorco/activetrail-python-sdk",
    packages=find_packages(exclude=["tests", "tests.*", "examples", "examples.*"]),
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    keywords="activetrail, sdk, email, marketing, sms, api",
    project_urls={
        "Documentation": "https://github.comEliorco/activetrail-python-sdk",
        "Source": "https://github.com/Eliorco/activetrail-python-sdk",
        "Tracker": "https://github.com/Eliorco/activetrail-python-sdk/issues",
    },
) 