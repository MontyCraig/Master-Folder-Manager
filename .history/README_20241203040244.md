# Enhanced Folder and Drive Manager

A powerful command-line tool for efficient file system and drive management across multiple volumes.

License: MetaReps Copyright 2024 - 2025

## Overview

Enhanced Folder Manager (EFM) is a professional-grade tool designed to help organize, analyze, and maintain complex file systems across multiple drives. It provides an intuitive interface for managing files, analyzing storage usage, and maintaining organized folder structures.

## Features & Development Status

### Phase 1: Core Features ✓
- [x] Interactive file and directory navigation
- [x] Multi-volume support and management
- [x] Smart file categorization
- [x] Bulk file organization
- [x] Storage analysis and reporting
- [x] Master folder management
- [ ] Git repository detection and management
- [ ] Duplicate file detection
- [ ] File comparison tools

### Phase 2: Advanced Features (In Progress)
- [ ] Hard drive management and monitoring
- [ ] Data cloning and replication
- [ ] Automated backup systems
- [ ] Cloud storage integration
- [ ] Scheduled operations
- [ ] Advanced search capabilities
- [ ] Custom categorization rules
- [ ] Batch processing operations

### Phase 3: Enterprise Features (Planned)
- [ ] Multi-user support
- [ ] Network drive integration
- [ ] Remote operation capabilities
- [ ] API interface
- [ ] Plugin system
- [ ] Custom workflow automation
- [ ] Advanced reporting and analytics

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

## Project Structure

```
enhanced-folder-manager/
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

## Development Roadmap

### Current Sprint
1. Core Functionality Enhancement
   - [ ] Improve volume management
   - [ ] Add search capabilities
   - [ ] Implement file comparison
   - [ ] Add Git integration

2. User Experience
   - [ ] Enhanced progress tracking
   - [ ] Better error messages
   - [ ] Command history
   - [ ] Quick access shortcuts

3. Testing & Documentation
   - [ ] Increase test coverage
   - [ ] Add integration tests
   - [ ] Improve documentation
   - [ ] Add usage examples

### Next Sprint
1. Advanced Features
   - [ ] Drive monitoring
   - [ ] Backup system
   - [ ] Cloud integration
   - [ ] Custom rules engine

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

## License

MetaReps Copyright 2024 - 2025



