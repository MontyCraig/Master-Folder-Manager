# Getting Started with Enhanced Folder Manager

## Introduction
Enhanced Folder Manager is a powerful tool for organizing and managing your files efficiently. This guide will help you get up and running quickly.

## Prerequisites
- Python 3.8 or higher
- Pydantic v2.0.0 or higher
- Click 8.0.0 or higher
- Rich 13.0.0 or higher
- pip (Python package installer)
- Basic knowledge of command line operations

## Installation

### Using pip
```bash
pip install enhanced-folder-manager
```

### From source
```bash
git clone https://github.com/MontyCraig/Master-Folder-Manager.git
cd master-folder-manager

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies and the package
pip install -r requirements.txt
pip install -e .
```

## Basic Usage

### Command Line Interface
The manager can be used from the command line:

```bash
# Get help
efm --help

# Analyze a directory
efm analyze ~/Documents

# Organize files by category
efm organize ~/Downloads --by-category

# Get file information
efm info ~/Documents/file.txt
```

### Python API
You can also use the manager in your Python code:

```python
from enhanced_folder_manager import FileManager

# Initialize manager
manager = FileManager()

# Get file info
file_info = manager.get_file_info("/path/to/file.txt")
if file_info.success:
    print(f"File size: {file_info.result.size} bytes")

# Move file safely
result = manager.safe_move_file(
    "/source/file.txt",
    "/dest/file.txt",
    overwrite=False
)
if result.success:
    print("File moved successfully")

# Analyze directory
stats = manager.analyze_directory("/path/to/dir")
if stats.success:
    print(f"Total files: {stats.result.file_count}")
```

## Configuration
The manager can be configured using a YAML file:

```yaml
# ~/.config/efm/config.yaml
categories:
  documents:
    extensions: [.pdf, .doc, .txt]
    description: Text documents
  
  images:
    extensions: [.jpg, .png, .gif]
    description: Image files

settings:
  organize_by_date: true
  create_symlinks: false
  backup_files: true
```

## Next Steps
1. Read the [Configuration Guide](./configuration.md) for detailed settings
2. Check out [Advanced Features](./advanced_features.md) for more capabilities
3. See [Troubleshooting](./troubleshooting.md) if you encounter issues

## Common Operations

### File Organization
```bash
# Organize by type
efm organize ~/Downloads --by-type

# Organize by date
efm organize ~/Pictures --by-date

# Custom organization
efm organize ~/Documents --config my_rules.yaml
```

### File Analysis
```bash
# Get directory statistics
efm analyze ~/Documents --detailed

# Find duplicate files
efm analyze ~/Downloads --find-duplicates

# Generate report
efm analyze ~/Pictures --report report.html
```

### File Operations
```bash
# Safe copy with verification
efm copy source.txt dest.txt --verify

# Secure delete
efm delete sensitive.txt --secure

# Batch rename
efm rename "*.jpg" "vacation_{n}.jpg"
```

## Tips and Best Practices

1. **Regular Organization**
   - Schedule regular organization of download folders
   - Use consistent category rules
   - Keep configuration backed up

2. **Performance**
   - Start with smaller directories while learning
   - Use `--dry-run` for testing operations
   - Consider using `--no-backup` for large operations

3. **Safety**
   - Always use `--backup` for important files
   - Test organization rules on sample data
   - Keep important files in separate directories

## Getting Help

- Use `efm --help` for command line help
- Check the [FAQ](./faq.md) for common questions
- Visit our [GitHub Issues](https://github.com/yourusername/master-folder-manager/issues) page
- Join our community on [Discord/Slack]

## Updating
To update to the latest version:

```bash
pip install --upgrade enhanced-folder-manager
```

## Uninstallation
If needed, you can uninstall:

```bash
pip uninstall enhanced-folder-manager
```

## Next Steps
- [Configuration Guide](./configuration.md)
- [Advanced Features](./advanced_features.md)
- [API Documentation](../api/core.md) 