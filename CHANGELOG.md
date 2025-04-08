# Changelog

## [1.1.0] - 2024-06-05

### Added
- Pydantic v2 compatibility
- Detailed documentation for Pydantic v2 migration
- New upgrade summary in technical documentation

### Changed
- Fixed operation_handler decorator to handle nested FileOperation objects
- Updated file operation functions to return proper values
- Modified test assertions for Path object comparisons
- Improved installation instructions in getting started guide

### Fixed
- Recursive model validation errors in FileOperation results
- Path object serialization in model_dump method
- Import dependencies in drive_ops.py
- Test failures due to Pydantic v2 validation changes

## [1.0.0] - 2024-04-08

### Added
- Initial release
- File and directory operations
- Multi-volume support
- Smart file categorization
- CLI interface
- Python API 