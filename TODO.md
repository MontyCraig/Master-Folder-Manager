# TODO - Master Folder Manager Roadmap

## High Priority

### Core Improvements

- [ ] Add async file operations for large batch processing
- [ ] Implement progress bars for bulk copy/move operations (Rich progress)
- [ ] Add dry-run mode to `organize_files()` that returns planned actions without executing
- [ ] Implement undo/rollback for file operations (operation journal)
- [ ] Add file deduplication using content hashing (md5/sha256)
- [ ] Support regex patterns in file search and filtering
- [ ] Add file watching mode (inotify/watchdog) for real-time organization

### CLI Enhancements

- [ ] Build full Click-based CLI with subcommands (analyze, organize, search, drives)
- [ ] Add `--verbose` and `--quiet` output modes
- [ ] Add `--format json` output option for scripting
- [ ] Implement interactive confirmation for destructive operations
- [ ] Add shell completion support (bash, zsh, fish)

### Testing

- [ ] Add integration tests for CLI commands
- [ ] Add property-based testing with Hypothesis for models
- [ ] Add benchmarks for large directory operations (1M+ files)
- [ ] Add cross-platform tests (Windows, macOS path handling)

## Medium Priority

### Configuration

- [ ] Support YAML configuration files in addition to JSON
- [ ] Add configuration validation on load with schema versioning
- [ ] Support XDG base directory specification for config location
- [ ] Add per-directory `.efm.json` override files
- [ ] Implement configuration migration between versions

### File Operations

- [ ] Add parallel file copy/move using concurrent.futures
- [ ] Implement incremental directory sync (rsync-like)
- [ ] Add file comparison (diff) between directories
- [ ] Support symbolic link handling policies (follow, skip, preserve)
- [ ] Add file metadata preservation during operations (xattr, ACLs)

### Organization

- [ ] Machine learning-based file categorization (content analysis)
- [ ] Custom rule engine for complex categorization logic
- [ ] Date-based organization (by year/month/day)
- [ ] Project detection (git repos, package.json, Cargo.toml)
- [ ] Tag-based organization system

### Storage Analysis

- [ ] Directory size treemap visualization (Rich or terminal graphics)
- [ ] Storage trend tracking over time
- [ ] Duplicate file finder with interactive resolution
- [ ] Large file finder with age-based recommendations
- [ ] Disk usage reports in multiple formats (HTML, JSON, CSV)

## Low Priority

### Architecture

- [ ] Add plugin system for custom file handlers
- [ ] REST API endpoint for programmatic access
- [ ] Web UI for visual file management
- [ ] Support for remote filesystems (SFTP, S3, WebDAV)
- [ ] Distributed operation mode for multi-server environments

### Performance

- [ ] Implement caching for directory scans (SQLite or mmap)
- [ ] Add memory-mapped I/O for large file hashing
- [ ] Profile and optimize hot paths (rglob, stat calls)
- [ ] Add connection pooling for remote filesystem operations

### Documentation

- [ ] Add API reference documentation (Sphinx/MkDocs)
- [ ] Create video tutorials for common workflows
- [ ] Add architecture decision records (ADRs)
- [ ] Write migration guide from v1.x to v2.x

### Developer Experience

- [ ] Add Makefile or justfile for common commands
- [ ] Set up GitHub Actions for automated releases
- [ ] Add Dependabot configuration for dependency updates
- [ ] Create Docker image for isolated usage
- [ ] Add VS Code devcontainer configuration

## Completed

- [x] Pydantic v2 migration with strict validation
- [x] Comprehensive test suite (107 tests, 98%+ coverage)
- [x] GitHub Actions CI/CD (tests + markdown lint)
- [x] Pre-commit hooks (ruff, mypy)
- [x] MIT License and open source documentation
- [x] Enterprise documentation suite (SECURITY.md, CONTRIBUTING.md, CODE_OF_CONDUCT.md)
- [x] Safe file operations with collision detection
- [x] Multi-volume support and drive scanning
- [x] Directory tree building with include/exclude patterns
- [x] File hashing with multiple algorithms (md5, sha1, sha256, sha512)
- [x] Configurable file categorization system
- [x] Interactive master folder selection (Rich prompts)
