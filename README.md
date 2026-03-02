# Master Folder Manager

A professional-grade CLI tool for organizing and managing files across multiple drives and volumes.

License: Sigma5C Corp. Copyright 2024 - 2026

## Overview

Master Folder Manager (MFM) is a powerful command-line interface tool designed to streamline file organization and management across multiple drives. It provides intelligent categorization, efficient file operations, and comprehensive drive management capabilities.

## Requirements

- Python 3.9 or higher
- Pydantic v2.0.0 or higher
- Click 8.0.0 or higher
- Rich 13.0.0 or higher
- Additional dependencies listed in requirements.txt

## Key Features

- Smart file categorization and organization
- Multi-volume support and management
- Bulk file operations with progress tracking
- Storage analysis and reporting
- Directory tree visualization
- Advanced search capabilities
- Secure file operations
- Drive space monitoring

## Installation

### From PyPI (Recommended)

```bash
pip install master-folder-manager
```

### From Source

```bash
# Clone the repository
git clone https://github.com/MontyCraig/Master-Folder-Manager.git
cd Master-Folder-Manager

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Install package in development mode
pip install -e .
```

## Usage

```bash
# Start the interactive interface
efm

# Analyze a directory
efm analyze ~/Documents

# Organize files by category
efm organize ~/Downloads --by-category

# Show help
efm --help
```

## Project Structure

```text
master-folder-manager/
├── src/                    # Source code
│   ├── core/              # Core functionality
│   │   ├── file_ops.py    # File operations
│   │   ├── dir_ops.py     # Directory operations
│   │   ├── models.py      # Pydantic data models
│   │   └── drive_ops.py   # Drive management
│   └── config/            # Configuration
│       └── settings.py    # Settings management
├── tests/                 # Test suite
└── docs/                  # Documentation
```

## Configuration

The tool maintains configuration in `~/.config/efm/config.yaml` including:

- Master folder locations
- Quick access volumes
- File categories
- Recent paths
- User preferences

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/MontyCraig/Master-Folder-Manager.git
cd Master-Folder-Manager

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install development dependencies
pip install -r requirements.txt

# Run tests
python -m pytest
```

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage report
python -m pytest --cov=src

# Run specific test file
python -m pytest tests/core/test_models.py
```

## Development Status

### Current Features

- [x] Interactive file and directory navigation
- [x] Multi-volume support and management
- [x] Smart file categorization
- [x] Bulk file organization
- [x] Storage analysis and reporting
- [x] Master folder management
- [x] Pydantic v2 compatibility

### Coming Soon

- [ ] Git repository detection
- [ ] Duplicate file detection
- [ ] File comparison tools
- [ ] Advanced search capabilities
- [ ] Custom categorization rules
- [ ] Batch processing operations

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

Sigma5C Corp. Copyright 2024 - 2026
