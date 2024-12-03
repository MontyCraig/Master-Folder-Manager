# Master Folder Manager

A professional-grade CLI tool for organizing and managing files across multiple drives and volumes.

License: MetaReps Copyright 2024 - 2025

## Overview

Master Folder Manager (MFM) is a powerful command-line interface tool designed to streamline file organization and management across multiple drives. It provides intelligent categorization, efficient file operations, and comprehensive drive management capabilities.

## Key Features

- 🗂️ Smart file categorization and organization
- 📁 Multi-volume support and management
- 🔄 Bulk file operations with progress tracking
- 📊 Storage analysis and reporting
- 🌲 Directory tree visualization
- 🔍 Advanced search capabilities
- 🔒 Secure file operations
- 📈 Drive space monitoring

## Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Install package
pip install -e .
```

## Usage

```bash
# Start the interactive interface
efm
```

## Project Structure

```
master-folder-manager/
├── src/                    # Source code
│   ├── core/              # Core functionality
│   │   ├── file_ops.py    # File operations
│   │   ├── dir_ops.py     # Directory operations
│   │   └── drive_ops.py   # Drive management
│   └── config/            # Configuration
│       └── settings.py    # Settings management
├── tests/                 # Test suite
└── docs/                  # Documentation
```

## Configuration

The tool maintains configuration in `~/.efm_config.json` including:
- Master folder locations
- Quick access volumes
- File categories
- Recent paths
- User preferences

## Development Status

### Current Features
- [x] Interactive file and directory navigation
- [x] Multi-volume support and management
- [x] Smart file categorization
- [x] Bulk file organization
- [x] Storage analysis and reporting
- [x] Master folder management

### Coming Soon
- [ ] Git repository detection
- [ ] Duplicate file detection
- [ ] File comparison tools
- [ ] Advanced search capabilities
- [ ] Custom categorization rules
- [ ] Batch processing operations

## License

MetaReps Copyright 2024 - 2025



