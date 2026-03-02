# Master Folder Manager - Professional File Organization CLI Tool

**Copyright 2024-2026 Sigma5C Corp. All rights reserved.**

## Overview

Master Folder Manager (MFM) is a professional-grade command-line interface tool designed for organizing and managing files across multiple drives and volumes within the Sigma5C cluster environment. Originally developed under Sigma5C Corp. Copyright 2024-2025, this tool has been integrated into the Sigma5C infrastructure for enterprise-level file management.

## Purpose

MFM provides intelligent file organization capabilities essential for managing the massive storage infrastructure of the Sigma5C cluster (12TB+ across multiple servers). The tool streamlines:

- Multi-drive file organization and categorization
- Bulk file operations with safety checks
- Storage analysis and capacity planning
- Directory structure management
- File search and retrieval across volumes

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
│   └── cli/                      # Command-line interface (if present)
├── tests/                        # Comprehensive test suite
│   ├── __init__.py
│   ├── pytest.ini               # Pytest configuration
│   ├── core/                    # Core functionality tests
│   └── integration/             # Integration tests
├── docs/                         # Documentation
│   ├── index.md                 # Main documentation
│   └── api/                     # API documentation (if present)
├── htmlcov/                      # Test coverage reports
├── coding_standards/             # Code quality standards
├── .github/                      # GitHub workflows and templates
├── .git/                         # Git repository
├── CHANGELOG.md                  # Version history
├── README.md                     # Project overview
├── requirements.txt              # Python dependencies
├── setup.py                      # Package installation script
├── .gitignore                    # Git ignore patterns
├── .cursorignore                 # Cursor IDE ignore patterns
├── .markdownlint.json            # Markdown linting config
├── .markdownlint-cli2.json       # Markdown CLI linting config
└── fix_markdown.py               # Markdown fixing utility
```

## Key Components

### Core Modules

#### file_ops.py

- File copying with progress tracking
- Safe file moving with collision detection
- Secure file deletion with confirmation
- File metadata management
- Integrity verification (checksums)

#### dir_ops.py

- Directory creation and management
- Recursive directory operations
- Directory tree traversal
- Symbolic link handling
- Permission management

#### models.py

- **Pydantic v2 data models** for type safety
- FileInfo: File metadata representation
- DirectoryInfo: Directory structure models
- DriveInfo: Storage volume information
- ConfigSettings: Application configuration models
- Validation and serialization

#### drive_ops.py

- Multi-volume detection and management
- Storage capacity monitoring
- Mount point tracking
- Drive health checks
- Space utilization analysis

### Configuration System

#### settings.py

- Configuration file location: `~/.config/efm/config.yaml`
- Master folder locations registry
- Quick access volume shortcuts
- File categorization rules
- Recent paths history
- User preferences and defaults

### Command-Line Interface

#### Primary Command: `efm`

- Interactive mode for guided operations
- Direct command mode for scripting
- Rich terminal output with colors and progress bars
- Context-aware help system

## Dependencies

### Python Requirements

- **Python**: 3.9 or higher (3.11+ recommended on Sigma5C)
- **Pydantic**: v2.0.0+ (modern data validation)
- **Click**: 8.0.0+ (CLI framework)
- **Rich**: 13.0.0+ (terminal formatting)
- Additional dependencies in requirements.txt

### System Requirements

- Linux/Unix environment (Ubuntu 24.04 LTS on Sigma5C)
- Sufficient permissions for file operations
- Access to target storage volumes
- Terminal with Unicode support (for Rich output)

### Sigma5C Integration

- Deployed on T430, R430, T620_1 servers
- Access to NFS-mounted storage volumes
- Integration with cluster file management policies

## Installation

### From Source (Sigma5C Standard)

```bash
# Navigate to project directory
cd /home/candc/Desktop/projects/master-folder-manager

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .

# Verify installation
efm --version
```

### From PyPI (Future)

```bash
# When published to PyPI
pip install master-folder-manager
```

### System-wide Installation (Sigma5C Cluster)

```bash
# Install for all users (requires sudo)
sudo pip install -e /home/candc/Desktop/projects/master-folder-manager

# Or create symbolic link to binary
sudo ln -s /home/candc/Desktop/projects/master-folder-manager/venv/bin/efm /usr/local/bin/efm
```

## Usage

### Interactive Mode

```bash
# Start interactive interface
efm

# Follow on-screen prompts for guided operations
```

### Direct Commands

#### Analyze Directory

```bash
# Analyze specific directory
efm analyze ~/Documents

# Analyze with detailed output
efm analyze ~/Documents --verbose

# Analyze entire drive
efm analyze /mnt/Storage12TB_1
```

#### Organize Files

```bash
# Organize by file category
efm organize ~/Downloads --by-category

# Organize by date
efm organize ~/Documents --by-date

# Organize by file type
efm organize ~/Pictures --by-type

# Dry-run (preview without changes)
efm organize ~/Downloads --by-category --dry-run
```

#### Drive Management

```bash
# List all drives
efm drives list

# Show drive details
efm drives info /mnt/Storage12TB_1

# Check drive space
efm drives space --all

# Monitor drive health
efm drives health /mnt/Storage12TB_1
```

#### Search Operations

```bash
# Search for files
efm search "*.pdf" --path ~/Documents

# Search by size
efm search --larger-than 100MB --path ~/Downloads

# Search by date
efm search --modified-after 2025-01-01 --path ~/Projects
```

#### Category Management

```bash
# List file categories
efm categories list

# Define custom category
efm categories add --name "Research" --extensions "pdf,doc,docx,tex"

# Apply category rules
efm categories apply --path ~/Downloads
```

### Configuration

```bash
# Show current configuration
efm config show

# Set master folder
efm config set master-folder /mnt/Storage12TB_1/MasterFiles

# Add quick access volume
efm config add-volume --name "Storage12TB" --path /mnt/Storage12TB_1

# Edit configuration file
efm config edit
```

### Help System

```bash
# General help
efm --help

# Command-specific help
efm organize --help
efm drives --help
efm search --help
```

## Integration with Sigma5C Systems

### Storage Infrastructure

- **T430**: 12TB primary storage (Storage12TB_1)
- **R430**: 125GB RAM server with storage management role
- **T620_1**: NFS exports and shared storage
- **R610**: Additional storage volumes via SSHFS

### File Organization Policies

1. **Project files**: Organized by project in `/home/candc/Desktop/projects/`
2. **Cluster management**: `/home/candc/Desktop/AllDrives/Storage12TB_1/Claude_Code_Max/`
3. **User data**: `/home/candc/Documents/`, `/home/candc/Downloads/`
4. **Shared storage**: NFS mounts accessible cluster-wide

### Backup Integration

- Pre-backup file organization
- Post-backup cleanup operations
- Duplicate file detection before backup
- Storage optimization for backup efficiency

### Automation Potential

```bash
# Cron job for automated organization (example)
# Daily at 2 AM: organize downloads
0 2 * * * /usr/local/bin/efm organize ~/Downloads --by-category --quiet

# Weekly: analyze drive space
0 3 * * 0 /usr/local/bin/efm drives space --all --report /var/log/drive-space.log
```

## Configuration

### Configuration File Location

```text
~/.config/efm/config.yaml
```

### Configuration Schema

```yaml
master_folders:
  - /mnt/Storage12TB_1/MasterFiles
  - /home/candc/Documents

quick_access_volumes:
  Storage12TB:
    path: /mnt/Storage12TB_1
    description: "Primary 12TB storage"
  R430_Data:
    path: /mnt/r430_storage
    description: "R430 server storage"

categories:
  documents:
    extensions: [pdf, doc, docx, odt, txt, md]
    target_folder: Documents
  images:
    extensions: [jpg, jpeg, png, gif, svg, webp]
    target_folder: Pictures
  code:
    extensions: [py, js, sh, c, cpp, java, go]
    target_folder: Code
  archives:
    extensions: [zip, tar, gz, bz2, 7z, rar]
    target_folder: Archives

recent_paths:
  - /home/candc/Downloads
  - /home/candc/Desktop/projects
  - /mnt/Storage12TB_1

preferences:
  confirm_deletions: true
  show_progress: true
  log_operations: true
  max_recent_paths: 10
  default_organize_method: by-category
```

## Development

### Setting Up Development Environment

```bash
# Clone repository (if pulling from external source)
git clone https://github.com/MontyCraig/Master-Folder-Manager.git
cd Master-Folder-Manager

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements.txt
pip install pytest pytest-cov black flake8 mypy

# Install pre-commit hooks (if available)
pre-commit install
```

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=src --cov-report=html

# Run specific test file
python -m pytest tests/core/test_models.py

# Run with verbose output
python -m pytest -v

# Run tests matching pattern
python -m pytest -k "test_file_ops"
```

### Code Quality

```bash
# Format code with black
black src/ tests/

# Lint with flake8
flake8 src/ tests/

# Type checking with mypy
mypy src/

# Run all quality checks
black src/ tests/ && flake8 src/ tests/ && mypy src/ && pytest
```

### Coverage Analysis

- Coverage reports generated in `htmlcov/` directory
- Current coverage: Check `.coverage` file
- Open `htmlcov/index.html` in browser for detailed coverage report

## Common Commands

### Quick Operations

```bash
# Quick analyze and organize workflow
efm analyze ~/Downloads && efm organize ~/Downloads --by-category

# Find and remove large files
efm search --larger-than 1GB --path ~/Downloads | xargs efm delete

# Backup before organizing
cp -r ~/Downloads ~/Downloads.backup && efm organize ~/Downloads --by-category

# Generate storage report
efm drives space --all --report ~/storage_report_$(date +%Y%m%d).txt
```

### Sigma5C Specific Commands

```bash
# Organize project files
efm organize /home/candc/Desktop/projects --by-project

# Clean up old Claude Code sessions
efm search "*.claude-session" --older-than 30d --path ~/.claude

# Analyze cluster storage usage
efm drives space /mnt/Storage12TB_1 /mnt/r430_storage /mnt/t620_nfs

# Find duplicate files before backup
efm duplicates find --path /home/candc/Documents --hash md5
```

## Troubleshooting

### Issue: Permission Denied

**Symptoms**: Cannot move/copy/delete files

**Solutions**:

```bash
# Check file permissions
ls -la <file>

# Check directory permissions
ls -la <directory>

# Fix ownership (if appropriate)
sudo chown -R candc:candc <directory>

# Fix permissions
chmod -R u+rwX <directory>
```

### Issue: Configuration Not Loading

**Symptoms**: Default settings used instead of custom config

**Solutions**:

```bash
# Check config file exists
ls -la ~/.config/efm/config.yaml

# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('~/.config/efm/config.yaml'))"

# Reset to defaults
efm config reset

# Recreate config directory
mkdir -p ~/.config/efm
efm config init
```

### Issue: Drive Not Detected

**Symptoms**: efm drives list doesn't show expected volumes

**Solutions**:

```bash
# Check mount points
df -h

# Check fstab entries
cat /etc/fstab

# Remount if needed
sudo mount -a

# Check for mount errors
dmesg | grep -i mount

# Update volume configuration
efm config add-volume --name "MissingDrive" --path /mnt/missing_drive
```

### Issue: Pydantic v2 Compatibility

**Symptoms**: Errors related to Pydantic models

**Solutions**:

```bash
# Check Pydantic version
pip show pydantic

# Upgrade to v2 if needed
pip install --upgrade 'pydantic>=2.0.0'

# Reinstall package
pip install -e . --force-reinstall
```

## Security Considerations

### File Operation Safety

- **Confirmation prompts**: Destructive operations require confirmation
- **Dry-run mode**: Preview operations before execution
- **Logging**: All operations logged for audit trail
- **Backup recommendations**: Always backup before bulk operations

### Permission Management

- Respects existing file permissions
- Preserves ownership during operations
- Warns when operations require elevated privileges
- Never escalates privileges without explicit user action

### Data Privacy

- No data transmitted externally
- Configuration stored locally
- No telemetry or usage tracking
- File contents never read unless explicitly required (hash calculations)

### Cluster Security Integration

- Coordinate with Eric864 (Security Lead) for policy compliance
- Respect cluster-wide file access policies
- Log operations for security audits
- Integration with Sigma5C security monitoring

## Maintenance

### Regular Tasks

#### Daily

- Monitor operation logs for errors
- Check configuration file integrity
- Verify drive access and mount points

#### Weekly

- Review and clean up organized files
- Update category rules if needed
- Check for software updates
- Analyze storage space trends

#### Monthly

- Comprehensive storage analysis across cluster
- Archive old logs
- Review and update quick access volumes
- Backup configuration file

### Update Procedure

```bash
# Pull latest changes (if from git)
cd /home/candc/Desktop/projects/master-folder-manager
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Run tests
python -m pytest

# Reinstall package
pip install -e .
```

## Related Projects

### Within Sigma5C

- **Change_Point**: Statistical analysis for file organization patterns
- **Chat_Bot_One**: AI-assisted file management queries
- **Predictive-Analytics**: Storage capacity prediction
- **October_28th_2025_Hardware_Audit**: Storage infrastructure inventory

### Related Tools

- **rsync**: Bulk file transfers between servers
- **ncdu**: Disk usage analysis
- **tree**: Directory structure visualization
- **fd-find**: Fast file searching
- **ripgrep**: Content searching

## Development Status

### Completed Features

- [x] Interactive file and directory navigation
- [x] Multi-volume support and management
- [x] Smart file categorization
- [x] Bulk file organization
- [x] Storage analysis and reporting
- [x] Master folder management
- [x] Pydantic v2 compatibility
- [x] Rich terminal output
- [x] Test coverage with pytest
- [x] Comprehensive documentation

### In Progress

- [ ] Git repository detection for code files
- [ ] Duplicate file detection with hashing
- [ ] File comparison tools
- [ ] Advanced search with regex support

### Planned Features

- [ ] Custom categorization rule builder
- [ ] Batch processing with job queues
- [ ] API endpoint for programmatic access
- [ ] Web UI for visual file management
- [ ] Integration with Sigma5C monitoring
- [ ] Machine learning for smart categorization
- [ ] Distributed operation across cluster
- [ ] Real-time directory watching

## Contact

- **Project Lead**: CandC (System Administrator)
- **Original Copyright**: Sigma5C Corp. 2024-2025
- **Current Owner**: Sigma5C Corp. 2024-2026
- **Email**: <sigma5ccorp@google.com>
- **Support**: <info@sigma5c.com>
- **Website**: sigma5c.com

## Notes

### Performance Considerations

- Large directory operations can be time-consuming
- Use `--dry-run` for preview on large datasets
- Consider using `nice` for background operations
- Monitor disk I/O during bulk operations

### Best Practices

1. **Always backup** before bulk organization
2. **Use dry-run mode** to preview changes
3. **Organize incrementally** rather than all at once
4. **Review logs** after operations
5. **Keep configuration updated** with current drives/volumes
6. **Test category rules** on small datasets first

### Known Limitations

- No support for Windows file systems (NTFS-specific features)
- Limited handling of special characters in filenames
- No built-in encryption support
- Single-threaded operations (no parallel processing yet)

### Changelog Highlights

- See CHANGELOG.md for detailed version history
- Pydantic v2 migration completed
- Enhanced error handling and logging
- Improved test coverage
- Documentation updates

---

This project is part of the Sigma5C infrastructure. For cluster-wide information, see `/home/candc/CLAUDE.md`.

Last Updated: March 2, 2026 | Document Version: 1.1 | Status: Active development and deployment
