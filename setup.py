"""Setup file for Master Folder Manager."""

from setuptools import setup, find_packages

setup(
    name="master-folder-manager",
    version="2.0.0",
    description="Professional-grade CLI tool for organizing and managing files across multiple drives",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Monty Craig",
    author_email="montycraig@users.noreply.github.com",
    url="https://github.com/MontyCraig/Master-Folder-Manager",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",
        "pathlib>=1.0.1",
        "rich>=13.0.0",
        "pydantic>=2.0.0",
        "psutil>=5.9.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.10.0",
            "mypy>=1.0.0",
            "ruff>=0.4.0",
            "pre-commit>=3.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "mfm=src.main:main",
        ],
    },
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: System :: Filesystems",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
)
