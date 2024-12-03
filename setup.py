"""
Setup file for Master Folder Manager.

License: MetaReps Copyright 2024 - 2025
"""

from setuptools import setup, find_packages

setup(
    name="master-folder-manager",
    version="0.1.0",
    description="Tool for managing files and folders across drives",
    author="MetaReps",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",
        "pathlib>=1.0.1",
        "rich>=10.0.0",
        "pydantic>=2.0.0",
        "psutil>=5.9.0",
    ],
    entry_points={
        'console_scripts': [
            'mfm=src.main:main',
        ],
    },
    python_requires=">=3.8",
) 