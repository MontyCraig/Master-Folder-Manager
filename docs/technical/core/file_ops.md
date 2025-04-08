# File Operations Technical Documentation

## Overview
This module provides a comprehensive set of file operations for the Enhanced Folder Manager. It includes functionality for file information retrieval, file manipulation, and cryptographic operations, with robust error handling and logging.

## Functions

### get_file_info
Retrieves detailed information about a file or directory.

#### Parameters
- `path` (Union[str, Path]):
  - Path to the file or directory
  - Can be string or Path object
  - Must be absolute path

#### Returns
- `FileOperation[FileInfo]`:
  - Success: FileInfo object with file details
  - Failure: Error message in FileOperation

#### Error Handling
- FileNotFoundError: File doesn't exist
- PermissionError: Insufficient permissions
- OSError: System-level file operation errors

#### Example
```python
result = get_file_info("/path/to/file.txt")
if result.success:
    file_info = result.result
    print(f"File size: {file_info.size} bytes")
else:
    print(f"Error: {result.error_message}")
```

### safe_move_file
Safely moves a file to a new location with validation and error handling.

#### Parameters
- `source` (Union[str, Path]):
  - Source file path
  - Must exist and be accessible

- `destination` (Union[str, Path]):
  - Destination file path
  - Parent directory created if needed

- `overwrite` (bool, optional):
  - Whether to overwrite existing files
  - Default: False

#### Returns
- `FileOperation[bool]`:
  - Success: True
  - Failure: Error message in FileOperation

#### Error Handling
- FileNotFoundError: Source doesn't exist
- FileExistsError: Destination exists (if not overwriting)
- PermissionError: Insufficient permissions
- OSError: System-level file operation errors

#### Example
```python
result = safe_move_file(
    "/source/file.txt",
    "/dest/file.txt",
    overwrite=True
)
if result.success:
    print("File moved successfully")
else:
    print(f"Error: {result.error_message}")
```

### safe_copy_file
Safely copies a file to a new location with validation and error handling.

#### Parameters
- `source` (Union[str, Path]):
  - Source file path
  - Must exist and be accessible

- `destination` (Union[str, Path]):
  - Destination file path
  - Parent directory created if needed

- `overwrite` (bool, optional):
  - Whether to overwrite existing files
  - Default: False

#### Returns
- `FileOperation[bool]`:
  - Success: True
  - Failure: Error message in FileOperation

#### Error Handling
- FileNotFoundError: Source doesn't exist
- FileExistsError: Destination exists (if not overwriting)
- PermissionError: Insufficient permissions
- OSError: System-level file operation errors

#### Example
```python
result = safe_copy_file(
    "/source/file.txt",
    "/dest/file.txt",
    overwrite=False
)
if result.success:
    print("File copied successfully")
else:
    print(f"Error: {result.error_message}")
```

### delete_file
Deletes a file or directory with optional secure deletion.

#### Parameters
- `path` (Union[str, Path]):
  - Path to delete
  - Can be file or directory

- `secure` (bool, optional):
  - Whether to perform secure deletion
  - Default: False
  - For files only, directories are removed normally

#### Returns
- `FileOperation[bool]`:
  - Success: True
  - Failure: Error message in FileOperation

#### Error Handling
- FileNotFoundError: Path doesn't exist
- PermissionError: Insufficient permissions
- OSError: System-level file operation errors

#### Example
```python
result = delete_file("/path/to/sensitive.txt", secure=True)
if result.success:
    print("File securely deleted")
else:
    print(f"Error: {result.error_message}")
```

### rename_file
Renames a file or directory.

#### Parameters
- `path` (Union[str, Path]):
  - Path to file/directory to rename
  - Must exist

- `new_name` (str):
  - New name (not path) for the file
  - Must be valid filename

#### Returns
- `FileOperation[Path]`:
  - Success: New Path object
  - Failure: Error message in FileOperation

#### Error Handling
- FileNotFoundError: Source doesn't exist
- FileExistsError: Destination exists
- ValueError: Invalid new name
- OSError: System-level file operation errors

#### Example
```python
result = rename_file("/path/to/old.txt", "new.txt")
if result.success:
    print(f"File renamed to: {result.result}")
else:
    print(f"Error: {result.error_message}")
```

### get_file_hash
Calculates cryptographic hash of a file.

#### Parameters
- `path` (Union[str, Path]):
  - Path to file to hash
  - Must be regular file

- `algorithm` (str, optional):
  - Hash algorithm to use
  - Default: "sha256"
  - Supported: md5, sha1, sha256, sha512

#### Returns
- `FileOperation[FileHash]`:
  - Success: FileHash object
  - Failure: Error message in FileOperation

#### Error Handling
- FileNotFoundError: File doesn't exist
- ValueError: Invalid algorithm
- PermissionError: Insufficient permissions
- OSError: System-level file operation errors

#### Example
```python
result = get_file_hash("/path/to/file.txt", algorithm="sha256")
if result.success:
    hash_info = result.result
    print(f"Hash: {hash_info.hash_value}")
else:
    print(f"Error: {result.error_message}")
```

## Error Handling Strategy
1. All functions use the `@operation_handler` decorator
2. Exceptions are caught and converted to FileOperation results
3. Detailed error messages are logged
4. Stack traces preserved in debug mode

## Logging
- All operations are logged using Python's logging module
- Log levels:
  - INFO: Successful operations
  - WARNING: Non-critical issues
  - ERROR: Operation failures
  - DEBUG: Detailed operation info

## Performance Considerations
1. Efficient file operations using `shutil`
2. Streaming file reading for large files
3. Proper file handle management
4. Minimal memory usage for large files

## Security Considerations
1. Path validation and normalization
2. Permission checking
3. Secure deletion option
4. No shell command execution

## Testing
Comprehensive test suite in `tests/core/test_file_ops.py`:
1. Unit tests for all functions
2. Integration tests for file operations
3. Error handling tests
4. Security tests
5. Performance tests for large files

## Dependencies
- Python standard library:
  - pathlib
  - shutil
  - hashlib
  - logging
- Project modules:
  - src.core.models
  - src.config 