# Master Folder Manager

A professional-grade CLI tool for organizing and managing files across multiple drives and volumes.

Licensed under the MIT License

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
python -m src.main

# Or, after installing in development mode:
mfm
```

The interactive menu provides options for:

- Listing directory contents
- Analyzing directories (size, extensions, categories)
- Creating and managing master folders
- Organizing files by category (move or copy)
- Browsing volumes
- Viewing directory trees

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

Configuration is stored in `~/.efm_config.json` and includes:

- Master folder root location
- Quick access volumes
- File categories with extensions and priorities
- Recent paths
- Excluded patterns (e.g., `.git`, `__pycache__`, `node_modules`)

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/MontyCraig/Master-Folder-Manager.git
cd Master-Folder-Manager

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install with development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Verify setup
python -m pytest
```

### Running Tests

```bash
# Run all tests with coverage
python -m pytest --cov=src --cov-report=term-missing

# Run specific test file
python -m pytest tests/core/test_models.py -v

# Run linting and type checks
ruff check src/ tests/
mypy src/
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

MIT License. Copyright 2024-2026 Monty Craig. See [LICENSE](LICENSE) for details.
