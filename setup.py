"""
Setup script for the ActiveTrail SDK.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="activetrail_sdk",
    version="1.0.0",
    author="Elior Cohen",
    author_email="eliorc1988@gmail.com",
    description="Unofficial Python SDK for ActiveTrail messageing service",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/actv_trail_sdk",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.28.2",
        "aiohttp>=3.8.0"    
    ],
    keywords=["activetrail", "api", "sdk", "email", "marketing"],
) 