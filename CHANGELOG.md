# Changelog

## [2.0.0] - 2026-03-02

### Added

- MIT License for open source distribution
- Enterprise documentation suite (SECURITY.md, CONTRIBUTING.md, CODE_OF_CONDUCT.md)
- TODO.md with full project roadmap
- GitHub issue templates (bug report, feature request)
- Pull request template with checklist
- Pre-commit hooks configuration (ruff, mypy, trailing whitespace)
- pyproject.toml with tool configurations
- .coveragerc with 95% minimum threshold
- Comprehensive test suite: 107 tests, 98%+ coverage
- Edge case tests for all core modules
- Test fixtures in conftest.py for shared setup
- PEP 561 py.typed marker

### Changed

- Dropped Python 3.8 support, minimum is now 3.9
- Added Python 3.12 and 3.13 to CI matrix
- Updated GitHub Actions to latest versions (checkout v4, setup-python v5, codecov v5)
- Fixed Node.js version for markdown lint (16 to 20)
- Replaced deprecated datetime.utcnow() with datetime.now(timezone.utc) in tests
- Updated setup.py with proper PyPI metadata and dev extras

### Fixed

- Markdown lint workflow crash (Node.js 16 incompatible with markdownlint-cli)
- Codecov upload failures (rate limiting, missing token)
- markdownlint config alias override bug (whitespace re-enabling MD012)
- Broken markdown code blocks and URLs in README.md
- 88 markdown lint errors across documentation files

### Removed

- Proprietary license headers from all source files
- Internal infrastructure references from documentation

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
