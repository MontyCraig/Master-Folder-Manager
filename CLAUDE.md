# Master Folder Manager - Development Guide

## Overview

Master Folder Manager (MFM) is a professional-grade command-line interface tool for organizing and managing files across multiple drives and volumes. It provides intelligent file categorization, efficient bulk operations, and comprehensive storage analysis.

## Directory Structure

```text
master-folder-manager/
├── src/                          # Source code
│   ├── core/                     # Core functionality modules
│   │   ├── file_ops.py          # File operations (copy, move, delete)
│   │   ├── dir_ops.py           # Directory operations
│   │   ├── models.py            # Pydantic v2 data models
│   │   └── drive_ops.py         # Multi-drive management
│   ├── config/                   # Configuration management
│   │   └── settings.py          # Settings and preferences
│   └── cli/                      # Command-line interface
├── tests/                        # Test suite (pytest)
│   ├── core/                    # Core module tests
│   └── conftest.py              # Shared test fixtures
├── docs/                         # Documentation
├── coding_standards/             # Code quality standards
├── .github/                      # GitHub workflows and templates
├── CHANGELOG.md                  # Version history
├── README.md                     # Project overview
├── CONTRIBUTING.md               # Contribution guidelines
├── SECURITY.md                   # Security policy
├── CODE_OF_CONDUCT.md            # Community code of conduct
├── TODO.md                       # Roadmap and planned features
├── LICENSE                       # MIT License
├── requirements.txt              # Python dependencies
├── setup.py                      # Package installation
├── pyproject.toml                # Build and tool configuration
├── .pre-commit-config.yaml       # Pre-commit hooks
├── .coveragerc                   # Coverage configuration
├── .markdownlint.json            # Markdown linting config
└── .gitignore                    # Git ignore patterns
```

## Key Components

### Core Modules

- **file_ops.py** - File copy/move/delete with progress tracking, integrity verification, collision detection
- **dir_ops.py** - Directory creation, recursive operations, tree traversal, file organization by category
- **models.py** - Pydantic v2 data models (FileInfo, DirectoryStats, FileOperation, FileHash, CategoryConfig)
- **drive_ops.py** - Multi-volume detection, storage monitoring, directory scanning, tree building

### Configuration

- **settings.py** - Configuration file management (~/.efm_config.json), file categorization rules, volume management, recent paths, interactive folder selection via Rich prompts

### Data Models (Pydantic v2)

- `FileInfo` - File metadata with path/name validation
- `DirectoryStats` - Directory analysis results with extension normalization
- `FileOperation` - Operation result wrapper with success/error tracking
- `FileHash` - File hash results with algorithm validation
- `CategoryConfig` - File category configuration with extension validation

## Dependencies

- **Python**: 3.9+
- **Pydantic**: v2.0.0+ (data validation)
- **Rich**: 13.0.0+ (terminal formatting)
- **psutil**: 5.9.0+ (system information)
- **Click**: 8.0.0+ (CLI framework)

## Development

### Setup

```bash
git clone https://github.com/MontyCraig/Master-Folder-Manager.git
cd Master-Folder-Manager
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
pre-commit install
```

### Running Tests

```bash
# All tests with coverage
python -m pytest --cov=src --cov-report=term-missing

# Specific module
python -m pytest tests/core/test_models.py -v

# With coverage HTML report
python -m pytest --cov=src --cov-report=html
```

### Code Quality

```bash
# Pre-commit runs automatically on commit, or manually:
pre-commit run --all-files

# Individual tools:
ruff check src/ tests/
ruff format src/ tests/
mypy src/
```

### Coverage

Current coverage: 98%+ across all modules. Coverage threshold set at 95% in `.coveragerc`.

## Configuration File

Default location: `~/.efm_config.json`

```json
{
    "master_folder_root": "/path/to/master/folders",
    "quick_access_volumes": ["/mnt/drive1", "/mnt/drive2"],
    "categories": {
        "Documents": {"extensions": [".pdf", ".doc", ".txt"], "priority": 1},
        "Images": {"extensions": [".jpg", ".png", ".gif"], "priority": 2},
        "Code": {"extensions": [".py", ".js", ".java"], "priority": 3}
    },
    "recent_paths": [],
    "favorites": [],
    "excluded_patterns": [".git", "__pycache__", "node_modules"]
}
```

## Usage

```bash
# Start interactive interface
efm

# Analyze directory
efm analyze ~/Documents

# Organize files by category
efm organize ~/Downloads --by-category

# List drives
efm drives list

# Search files
efm search "*.pdf" --path ~/Documents
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. All contributions must include tests and pass CI checks.

## License

MIT License. See [LICENSE](LICENSE) for details.
