# Core Models Technical Documentation

## Overview

This document provides technical details about the data models used in the Enhanced Folder Manager. These models are implemented using Pydantic for robust data validation, serialization, and documentation.

## Models

### FileInfo

Represents detailed information about a file or directory in the system.

#### Fields

- `name` (str):

  - File or directory name

  - Constraints: 1-255 characters, no path separators or invalid characters

  - Example: "document.txt"

- `path` (str):

  - Absolute path to the file

  - Must be a valid, absolute filesystem path

  - Example: "/home/user/documents/document.txt"

- `size` (int):

  - File size in bytes

  - Constraints: ≥ 0

  - Example: 1024

- `modified` (datetime):

  - Last modification timestamp

  - UTC timezone

- `is_dir` (bool):

  - Whether the item is a directory

- `is_file` (bool):

  - Whether the item is a regular file

- `category` (Optional[str]):

  - File category based on extension

  - Example: "document", "image", "video"

#### Validation Rules

1. Filename validation:

   - No empty or whitespace-only names

   - No path separators (/ or \)

   - No invalid characters (<>:"|?*)



2. Path validation:

   - Must be absolute path

   - No directory traversal (..)

   - Path normalization

### DirectoryStats

Tracks statistics about a directory's contents.

#### Fields

- `total_size` (int):

  - Total size of all files in bytes

  - Constraints: ≥ 0

- `file_count` (int):

  - Number of files

  - Constraints: ≥ 0

- `dir_count` (int):

  - Number of directories

  - Constraints: ≥ 0

- `extensions` (Dict[str, int]):

  - Count of file extensions

  - Keys are lowercase extensions with dot

  - Example: {".txt": 3, ".jpg": 5}

- `by_category` (Dict[str, Dict[str, int]]):

  - Files grouped by category

  - Example: {"documents": {"count": 5, "size": 512000}}

#### Validation Rules

1. All counts must be non-negative

2. Extensions are normalized to lowercase

3. Categories must match predefined categories

### FileOperation

Represents the result of a file operation.

#### Fields

- `success` (bool):

  - Whether the operation succeeded

- `error_message` (Optional[str]):

  - Error message if operation failed

  - None if successful

- `result` (Optional[Union[str, Path, Dict[str, Any]]]):

  - Operation-specific result data

  - Type varies by operation

### FileHash

Represents a file's cryptographic hash.

#### Fields

- `algorithm` (str):

  - Hash algorithm used

  - Allowed values: md5, sha1, sha256, sha512

  - Regex validation: ^(md5|sha1|sha256|sha512)$

- `hash_value` (str):

  - Computed hash value

  - Constraints: 32-128 characters (depending on algorithm)

  - Must be valid hexadecimal

- `file_path` (str):

  - Path to the hashed file

#### Validation Rules

1. Algorithm validation:

   - Must be one of supported algorithms

   - Case-insensitive matching



2. Hash validation:

   - Length must match algorithm (MD5: 32, SHA-1: 40, etc.)

   - Must contain only hexadecimal characters

   - Normalized to lowercase

### CategoryConfig

Defines a file category and its associated extensions.

#### Fields

- `name` (str):

  - Category name

  - Constraints: 1-50 characters

- `extensions` (List[str]):

  - File extensions for this category

  - Normalized to lowercase with leading dot

  - Example: [".pdf", ".doc", ".txt"]

- `description` (Optional[str]):

  - Category description

  - Max length: 200 characters

#### Validation Rules

1. Extension validation:

   - Must be valid format (alphanumeric with dot)

   - Normalized to lowercase

   - Leading dot added if missing

## Usage Examples

```python

# Creating a FileInfo instance

file_info = FileInfo(
    name="document.txt",
    path="/home/user/documents/document.txt",
    size=1024,
    modified=datetime.utcnow(),
    is_dir=False,
    is_file=True,
    category="document"
)

# Creating DirectoryStats

stats = DirectoryStats(
    total_size=1048576,
    file_count=10,
    dir_count=2,
    extensions={".txt": 3, ".jpg": 5},
    by_category={
        "documents": {"count": 5, "size": 512000}
    }
)

# File operation result

operation = FileOperation(
    success=True,
    result="/path/to/processed/file.txt"
)

# File hash

hash_info = FileHash(
    algorithm="sha256",
    hash_value="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    file_path="/path/to/file.txt"
)

# Category configuration

category = CategoryConfig(
    name="documents",
    extensions=[".pdf", ".doc", ".txt"],
    description="Text-based document files"
)

```text
## Error Handling

All models include comprehensive error handling:

1. ValidationError for invalid input

2. Detailed error messages

3. Type conversion errors

4. Custom validation errors

## Performance Considerations

1. Efficient regex patterns for validation

2. Cached property access

3. Optimized JSON serialization

4. Minimal memory footprint

## Security Considerations

1. Path traversal protection

2. Filename sanitization

3. Input length limits

4. Secure hash handling

## Testing

All models have comprehensive test coverage:

1. Unit tests for all validation rules

2. Edge case testing

3. Performance testing

4. Security testing

See `tests/core/test_models.py` for detailed test cases.
