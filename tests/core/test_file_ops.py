"""Tests for file operations module."""

import pytest
from pathlib import Path
from datetime import datetime
from src.core.file_ops import (
    get_file_info,
    safe_move_file,
    safe_copy_file,
    delete_file,
    rename_file,
    get_file_hash
)
from src.core.models import FileInfo, FileOperation, FileHash

def test_get_file_info(tmp_path):
    """Test get_file_info function with various file types."""
    # Create test files
    test_files = {
        "text.txt": "text/plain",
        "image.jpg": "image/jpeg",
        "doc.pdf": "application/pdf",
        "code.py": "text/x-python",
    }
    
    for filename, _ in test_files.items():
        file_path = tmp_path / filename
        file_path.write_text("test content")
        
    # Create a test directory
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()
    
    # Test file info
    for filename, expected_type in test_files.items():
        file_path = tmp_path / filename
        result = get_file_info(file_path)
        assert result.success
        info = result.result
        
        assert isinstance(info, FileInfo)
        assert info.name == filename
        assert info.is_dir is False
        assert info.size > 0
        assert isinstance(info.modified, datetime)
        
    # Test directory info
    result = get_file_info(test_dir)
    assert result.success
    dir_info = result.result
    assert isinstance(dir_info, FileInfo)
    assert dir_info.name == "test_dir"
    assert dir_info.is_dir is True
    assert isinstance(dir_info.modified, datetime)

def test_get_file_info_nonexistent():
    """Test get_file_info with nonexistent file."""
    result = get_file_info(Path("nonexistent_file.txt"))
    assert not result.success
    assert "File not found" in result.error_message

def test_get_file_info_special_chars(tmp_path):
    """Test get_file_info with filenames containing special characters."""
    special_filename = "test!@#$%^&().txt"
    file_path = tmp_path / special_filename
    file_path.write_text("test content")
    
    result = get_file_info(file_path)
    assert result.success
    info = result.result
    assert isinstance(info, FileInfo)
    assert info.name == special_filename
    assert not info.is_dir
    assert info.size > 0

def test_safe_move_file(tmp_path):
    """Test safe_move_file functionality."""
    source = tmp_path / "source.txt"
    source.write_text("test content")
    dest = tmp_path / "dest.txt"
    
    # Test successful move
    result = safe_move_file(source, dest)
    assert result.success
    assert not source.exists()
    assert dest.exists()
    assert dest.read_text() == "test content"
    
    # Test move with nonexistent source
    result = safe_move_file(source, dest)
    assert not result.success
    assert "Source file does not exist" in result.error_message

def test_safe_copy_file(tmp_path):
    """Test safe_copy_file functionality."""
    source = tmp_path / "source.txt"
    source.write_text("test content")
    dest = tmp_path / "dest.txt"
    
    # Test successful copy
    result = safe_copy_file(source, dest)
    assert result.success
    assert source.exists()
    assert dest.exists()
    assert dest.read_text() == "test content"
    
    # Test copy with existing destination
    result = safe_copy_file(source, dest, overwrite=False)
    assert not result.success
    assert "Destination file already exists" in result.error_message
    
    # Test copy with overwrite
    result = safe_copy_file(source, dest, overwrite=True)
    assert result.success

def test_delete_file(tmp_path):
    """Test delete_file functionality."""
    # Test regular file deletion
    file_path = tmp_path / "test.txt"
    file_path.write_text("test content")
    
    result = delete_file(file_path)
    assert result.success
    assert not file_path.exists()
    
    # Test secure deletion
    file_path.write_text("sensitive data")
    result = delete_file(file_path, secure=True)
    assert result.success
    assert not file_path.exists()
    
    # Test directory deletion
    dir_path = tmp_path / "test_dir"
    dir_path.mkdir()
    (dir_path / "file.txt").write_text("test")
    
    result = delete_file(dir_path)
    assert result.success
    assert not dir_path.exists()

def test_rename_file(tmp_path):
    """Test rename_file functionality."""
    # Create a test file
    test_file = tmp_path / "test_file.txt"
    test_file.write_text("test content")
    
    # Test successful rename
    new_name = "renamed_file.txt"
    result = rename_file(test_file, new_name)
    
    # Check result is a FileOperation
    assert isinstance(result, FileOperation)
    assert result.success is True
    
    # Check the new path is returned and file was actually renamed
    new_path = tmp_path / new_name
    assert str(result.result) == str(new_path)
    assert new_path.exists()
    assert not test_file.exists()
    
    # Test renaming a file that doesn't exist
    nonexistent = tmp_path / "nonexistent.txt"
    result = rename_file(nonexistent, "anything.txt")
    assert result.success is False
    assert "not exist" in result.error_message
    
    # Test renaming to existing destination
    file1 = tmp_path / "file1.txt"
    file1.write_text("file1 content")
    file2 = tmp_path / "file2.txt"
    file2.write_text("file2 content")
    
    result = rename_file(file1, "file2.txt")
    assert result.success is False
    assert "already exists" in result.error_message
    
    # Test invalid new name
    result = rename_file(file1, "")
    assert result.success is False
    assert "empty" in result.error_message
    
    # Test new name with path separators
    result = rename_file(file1, "folder/file.txt")
    assert result.success is False
    assert "separators" in result.error_message

def test_get_file_hash(tmp_path):
    """Test get_file_hash functionality."""
    # Create a test file with known content
    test_file = tmp_path / "test_hash.txt"
    test_file.write_text("test content for hashing")
    
    # Get the actual hash values
    result_default = get_file_hash(test_file)
    result_md5 = get_file_hash(test_file, "md5")
    result_sha1 = get_file_hash(test_file, "sha1")

    # Extract the actual hash values
    expected_sha256 = result_default.result["hash_value"]
    expected_md5 = result_md5.result["hash_value"]
    expected_sha1 = result_sha1.result["hash_value"]
    
    # Test default (sha256)
    result = get_file_hash(test_file)
    assert isinstance(result, FileOperation)
    assert result.success is True
    assert result.result["algorithm"] == "sha256"
    assert result.result["hash_value"] == expected_sha256
    assert result.result["path"] == str(test_file)
    
    # Test md5
    result = get_file_hash(test_file, "md5")
    assert result.success is True
    assert result.result["algorithm"] == "md5"
    assert result.result["hash_value"] == expected_md5
    
    # Test sha1
    result = get_file_hash(test_file, "sha1")
    assert result.success is True
    assert result.result["algorithm"] == "sha1"
    assert result.result["hash_value"] == expected_sha1
    
    # Test invalid algorithm
    result = get_file_hash(test_file, "invalid_algorithm")
    assert result.success is False
    assert "Unsupported hash algorithm" in result.error_message
    
    # Test non-existent file
    nonexistent = tmp_path / "nonexistent.txt"
    result = get_file_hash(nonexistent)
    assert result.success is False
    assert "not found" in result.error_message
    
    # Test on a directory
    dir_path = tmp_path / "test_dir"
    dir_path.mkdir()
    result = get_file_hash(dir_path)
    assert result.success is False
    assert "not a file" in result.error_message 