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
    file_path = tmp_path / "old.txt"
    file_path.write_text("test content")
    
    # Test successful rename
    result = rename_file(file_path, "new.txt")
    assert result.success
    new_path = result.result
    assert not file_path.exists()
    assert new_path.exists()
    assert new_path.name == "new.txt"
    
    # Test rename with invalid characters
    result = rename_file(new_path, "invalid/name.txt")
    assert not result.success
    assert "filename contains path separators" in result.error_message.lower()

def test_get_file_hash(tmp_path):
    """Test get_file_hash functionality."""
    file_path = tmp_path / "test.txt"
    file_path.write_text("test content")
    
    # Test with default algorithm (sha256)
    result = get_file_hash(file_path)
    assert result.success
    hash_info = result.result
    assert isinstance(hash_info, FileHash)
    assert hash_info.algorithm == "sha256"
    assert len(hash_info.hash_value) == 64  # SHA-256 produces 64 character hashes
    
    # Test with different algorithms
    for algorithm in ["md5", "sha1", "sha512"]:
        result = get_file_hash(file_path, algorithm)
        assert result.success
        assert result.result.algorithm == algorithm
    
    # Test with invalid algorithm
    result = get_file_hash(file_path, "invalid")
    assert not result.success
    assert "Unsupported hash algorithm" in result.error_message 