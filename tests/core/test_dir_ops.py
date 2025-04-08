"""Tests for directory operations module."""

import pytest
from pathlib import Path
from src.core.dir_ops import ensure_master_folders, analyze_directory, organize_files

def test_ensure_master_folders(tmp_path):
    """Test creation of master folders."""
    # Test default master folders creation
    master_path = tmp_path / "master"
    ensure_master_folders(master_path)
    
    # Check if default folders exist
    expected_folders = [
        "Documents",
        "Images",
        "Videos",
        "Music",
        "Downloads",
        "Archives",
        "Code",
        "Other"
    ]
    
    for folder in expected_folders:
        assert (master_path / folder).is_dir()

def test_analyze_directory(tmp_path):
    """Test directory analysis functionality."""
    # Create test files
    (tmp_path / "test.txt").write_text("test content")
    (tmp_path / "test.jpg").write_bytes(b"fake image content")
    (tmp_path / "subdir").mkdir()
    (tmp_path / "subdir" / "test.py").write_text("print('hello')")
    
    stats = analyze_directory(tmp_path)
    
    assert stats["file_count"] == 3
    assert stats["dir_count"] == 1
    assert stats["total_size"] > 0
    assert len(stats["extensions"]) == 3
    assert ".txt" in stats["extensions"]
    assert ".jpg" in stats["extensions"]
    assert ".py" in stats["extensions"]

def test_organize_files(tmp_path):
    """Test file organization functionality."""
    # Create source directory with test files
    source = tmp_path / "source"
    source.mkdir()
    
    # Create test files
    (source / "doc.txt").write_text("test content")
    (source / "image.jpg").write_bytes(b"fake image content")
    (source / "script.py").write_text("print('hello')")
    
    # Create destination directory
    dest = tmp_path / "dest"
    dest.mkdir()
    
    # Organize files
    organize_files(source, dest)
    
    # Check if files are organized correctly
    assert (dest / "Documents" / "doc.txt").exists()
    assert (dest / "Images" / "image.jpg").exists()
    assert (dest / "Code" / "script.py").exists()

def test_organize_files_with_duplicates(tmp_path):
    """Test file organization with duplicate files."""
    source = tmp_path / "source"
    source.mkdir()
    
    # Create duplicate files
    (source / "test1.txt").write_text("same content")
    (source / "test2.txt").write_text("same content")
    
    dest = tmp_path / "dest"
    dest.mkdir()
    
    organize_files(source, dest)
    
    # Check if both files are preserved with different names
    files = list((dest / "Documents").glob("*.txt"))
    assert len(files) == 2
    assert files[0].name != files[1].name 