# TODO - Master Folder Manager Roadmap

## Critical - Runtime Bugs

These are defects that cause crashes or incorrect behavior in the current codebase.

- [ ] **Fix `list_directory_contents()` crash** (main.py:215-220): `get_file_info()` returns a `FileOperation` object, but the code accesses it as a dict (`info["name"]`, `info["is_dir"]`, etc.). This crashes immediately on use.
- [ ] **Fix `build_directory_tree()` console.print crash** (main.py:349,355): `build_directory_tree()` returns a plain `dict`, not a Rich renderable. Passing it to `console.print()` does not produce a tree display.
- [ ] **Unify dual category systems**: `dir_ops.DEFAULT_CATEGORIES` (8 categories, flat list) and `settings.DEFAULT_CONFIG["categories"]` (8 different categories, nested dict with priority) are completely independent. `organize_files()` uses `dir_ops` categories while `get_category_for_file()` uses `settings` categories, producing different results for the same file.
- [ ] **Fix entry point mismatch**: `setup.py` defines entry point as `mfm`, but all documentation and CLAUDE.md reference `efm`. Pick one and make it consistent everywhere.

## High Priority - Missing Functionality

Features that are documented or expected but do not exist.

- [ ] **Implement Click CLI**: Click is imported in `main.py` but never used. The entire documented CLI (`efm analyze`, `efm organize`, `efm drives list`, `efm search`) does not exist. The tool only has the Rich interactive menu.
- [ ] **Implement 5 stub menu items**: Search Folders (option 6), Recent Folders (option 8), Compare Directories (option 9), Find Duplicates (option 10), and Git Operations (option 11) all display "coming soon" and do nothing.
- [ ] **Add symlink handling**: No symlink detection or policy anywhere. `rglob("*")` follows symlinks by default, risking infinite loops on circular symlinks and processing files outside the intended scope.
- [ ] **Remove or integrate `path_manager.py`**: Dead code with hardcoded macOS volume paths (`/Volumes/Seagate_2`, `/Volumes/Willie`, etc.). Never imported anywhere. Either delete it or integrate its sanitization concept properly.
- [ ] **Add main.py test coverage**: Zero tests for `main.py` (386 lines). The `.coveragerc` currently excludes it entirely. Needs at minimum: unit tests for each menu handler, integration tests for the main loop.

## High Priority - Security

- [ ] **Fix path traversal detection**: `models.py` validates filenames for `..` and path separators, but this only applies to `FileInfo.name`. Directory paths passed to `analyze_directory()`, `organize_files()`, `scan_directory()`, and `build_directory_tree()` have zero validation. Add path validation at all public API boundaries.
- [ ] **Add symlink attack prevention**: `organize_files()` uses `shutil.move/copy2` which follow symlinks. A malicious symlink in the source directory could cause writes outside the destination. Use `Path.resolve()` and verify the resolved path is within expected boundaries before operations.
- [ ] **Strengthen secure deletion** (file_ops.py:148-163): Currently overwrites with `os.urandom()` once. For sensitive data, implement multi-pass overwrite (DoD 5220.22-M or similar) and add `fsync()` to ensure overwrite hits disk before unlink.
- [ ] **Add permission checks before operations**: No pre-flight permission validation. Operations fail mid-way through bulk processing if a single file lacks permissions. Check read/write permissions before starting batch operations.
- [ ] **Sanitize error messages**: Exception messages (e.g., in `FileOperation.error_message`) may leak full file paths. Sanitize paths in user-facing error output.

## High Priority - Performance

- [ ] **Cache config loading**: `settings.load_config()` reads and parses `~/.efm_config.json` from disk on every call. In `organize_files()`, `get_category_for_file()` is called per-file, each triggering a full disk read + JSON parse. Add in-memory caching with TTL or load-once-per-operation pattern.
- [ ] **Add parallel I/O for bulk operations**: `organize_files()`, `analyze_directory()`, and `scan_directory()` are all single-threaded sequential loops. Use `concurrent.futures.ThreadPoolExecutor` for I/O-bound file operations.
- [ ] **Increase hash buffer size** (file_ops.py): Currently uses default `read()` block size. Use 64KB-1MB chunks for `get_file_hash()` to reduce syscall overhead on large files.
- [ ] **Reduce Pydantic overhead in stat-gathering**: `get_file_info()` constructs a full `FileInfo` Pydantic model with validation for every file encountered during directory scans. For bulk operations, consider a lightweight dataclass or namedtuple alternative.
- [ ] **Add generator-based directory iteration**: `scan_directory()` and `analyze_directory()` build full result lists in memory. For directories with millions of files, use generators/iterators to reduce memory footprint.

## Medium Priority - Architecture

- [ ] **Remove hardcoded macOS paths from DEFAULT_CONFIG** (settings.py:16-25): Default volumes reference `/Volumes/Seagate_2`, `/Volumes/MongoDB`, etc. These are personal development paths. Use platform-appropriate defaults (`~/Documents` on all platforms, auto-detect mounted volumes).
- [ ] **Consolidate category definitions**: Merge `dir_ops.DEFAULT_CATEGORIES` and `settings.DEFAULT_CONFIG["categories"]` into a single source of truth. All code paths should reference one canonical category registry.
- [ ] **Add proper logging configuration**: Logging is configured with `getLogger(__name__)` in every module but never configured at the application level. Add root logger setup in main.py or a dedicated logging config.
- [ ] **Add type stubs for public API**: While `py.typed` marker exists, the actual type annotations are incomplete (many `Dict[str, Any]` that could be `TypedDict` or proper model types).
- [ ] **Replace `os.chdir()` in menu handler** (main.py:371): Changing global process working directory as a user action is error-prone. Track the "current volume" as application state instead.

## Medium Priority - CLI and UX

- [ ] **Add `--dry-run` mode**: `organize_files()` immediately moves/copies files. Add a preview mode that shows planned operations without executing.
- [ ] **Add `--verbose` and `--quiet` output modes**: No output level control currently exists.
- [ ] **Add `--format json` output**: No machine-readable output option for scripting and automation.
- [ ] **Add progress bars for bulk operations**: Rich is imported but progress bars are not used during file copy/move/organize operations.
- [ ] **Add shell completion**: No bash/zsh/fish completion support despite using Click.
- [ ] **Add confirmation prompts for destructive operations**: `secure_delete()` has no confirmation. Bulk `organize_files()` with `move_files=True` can relocate thousands of files with a single "y".

## Medium Priority - Testing

- [ ] **Add symlink tests**: Zero tests verify symlink handling (following, skipping, circular detection).
- [ ] **Add Unicode/special character filename tests**: No tests for files with emoji, CJK characters, or control characters in names.
- [ ] **Add large directory benchmarks**: No performance tests for operations on directories with 10K+ files.
- [ ] **Add cross-platform path tests**: All tests use POSIX paths. No Windows path separator or drive letter handling tests.
- [ ] **Add property-based testing with Hypothesis**: Models have validators that could benefit from fuzz testing.
- [ ] **Add integration tests for the interactive menu**: `main.py` is entirely untested.
- [ ] **Test the dual category system divergence**: No test verifies that `dir_ops` and `settings` categories produce the same results.

## Medium Priority - Configuration

- [ ] **Support XDG base directory specification**: Config hardcoded to `~/.efm_config.json`. Should respect `$XDG_CONFIG_HOME` on Linux, `%APPDATA%` on Windows.
- [ ] **Add configuration schema versioning**: No version field in config. Adding new fields requires manual migration.
- [ ] **Add per-directory `.efm.json` override files**: No way to customize behavior per-directory.
- [ ] **Support YAML configuration**: Only JSON currently supported.
- [ ] **Add `--config` CLI flag**: No way to specify alternative config file path.

## Medium Priority - File Operations

- [ ] **Add incremental directory sync**: No rsync-like comparison or delta operations.
- [ ] **Add file comparison between directories**: No diff capability.
- [ ] **Add file metadata preservation**: `shutil.copy2` preserves some metadata, but no explicit handling of xattr, ACLs, or alternate data streams.
- [ ] **Add undo/rollback for file operations**: No operation journal or transaction log. Interrupted bulk operations leave files in an inconsistent state.
- [ ] **Add file deduplication**: Content hashing exists (`get_file_hash`) but no dedup workflow.

## Low Priority - Documentation

- [ ] **Add API reference docs**: No Sphinx/MkDocs documentation for the Python API.
- [ ] **Add architecture decision records (ADRs)**: No documentation for design choices.
- [ ] **Write migration guide v1.x to v2.x**: No upgrade documentation exists.
- [ ] **Add man page**: No system-level documentation.
- [ ] **Update docs to match actual capabilities**: Current README documents CLI commands (`efm analyze`, `efm search`) that do not exist.

## Low Priority - Developer Experience

- [ ] **Add Makefile or justfile**: No task runner for common development commands.
- [ ] **Set up automated releases**: No GitHub Actions workflow for PyPI publishing or GitHub Releases.
- [ ] **Add Docker image**: No containerized distribution.
- [ ] **Add VS Code devcontainer**: No container-based development environment.
- [ ] **Add CODEOWNERS file**: No automatic PR reviewer assignment.

## Low Priority - Future Features

- [ ] **File watching mode**: Real-time organization using inotify/watchdog.
- [ ] **Plugin system**: Custom file handlers for specialized file types.
- [ ] **REST API**: Programmatic access for integration with other tools.
- [ ] **Web UI**: Browser-based file management interface.
- [ ] **Remote filesystem support**: SFTP, S3, WebDAV integration.
- [ ] **Machine learning categorization**: Content-based file classification beyond extension matching.
- [ ] **Tag-based organization**: User-defined tags independent of file categories.
- [ ] **Storage trend tracking**: Historical disk usage analysis over time.

## Completed

- [x] Pydantic v2 migration with strict validation
- [x] Comprehensive test suite (107 tests, 98%+ coverage)
- [x] GitHub Actions CI/CD (tests on Python 3.9-3.13 + markdown lint)
- [x] Pre-commit hooks (ruff, mypy, trailing whitespace, YAML/JSON validation)
- [x] MIT License and open source documentation
- [x] Enterprise documentation suite (SECURITY.md, CONTRIBUTING.md, CODE_OF_CONDUCT.md)
- [x] GitHub issue and PR templates
- [x] Dependabot configuration for dependency updates
- [x] Safe file operations with collision detection
- [x] Multi-volume support and drive scanning
- [x] Directory tree building with include/exclude patterns
- [x] File hashing with multiple algorithms (md5, sha1, sha256, sha512)
- [x] Configurable file categorization system
- [x] Interactive master folder selection (Rich prompts)
- [x] PEP 561 py.typed marker
- [x] pyproject.toml with unified tool configuration
