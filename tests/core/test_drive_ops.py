"""Tests for drive operations module."""

import pytest
from pathlib import Path
from src.core.drive_ops import get_all_volumes, scan_directory, build_directory_tree

def test_get_all_volumes(monkeypatch):
    """Test volume detection functionality."""
    # Mock psutil.disk_partitions
    def mock_disk_partitions(all=False):
        return [
            type('MockDiskPartition', (), {
                'device': '/dev/sda1',
                'mountpoint': '/',
                'fstype': 'ext4',
                'opts': 'rw,relatime'
            }),
            type('MockDiskPartition', (), {
                'device': '/dev/sdb1',
                'mountpoint': '/home',
                'fstype': 'ext4',
                'opts': 'rw,relatime'
            })
        ]
    
    # Mock psutil.disk_usage
    def mock_disk_usage(path):
        return type('MockDiskUsage', (), {
            'total': 1000000,
            'used': 500000,
            'free': 500000
        })
    
    import psutil
    monkeypatch.setattr(psutil, 'disk_partitions', mock_disk_partitions)
    monkeypatch.setattr(psutil, 'disk_usage', mock_disk_usage)
    
    volumes = get_all_volumes()
    assert len(volumes) == 2
    assert volumes[0]["mount_point"] == "/"
    assert volumes[1]["mount_point"] == "/home"
    assert all(v["fstype"] == "ext4" for v in volumes)
    assert all(v["used"] == 500000 for v in volumes)
    assert all(v["free"] == 500000 for v in volumes)

def test_scan_directory(tmp_path):
    """Test directory scanning functionality."""
    # Create test directory structure
    (tmp_path / "dir1").mkdir()
    (tmp_path / "dir1" / "file1.txt").write_text("content")
    (tmp_path / "dir2").mkdir()
    (tmp_path / "dir2" / "subdir").mkdir()
    (tmp_path / "dir2" / "subdir" / "file2.txt").write_text("content")
    
    scan_results = scan_directory(tmp_path)
    
    assert len(scan_results["files"]) == 2
    assert len(scan_results["dirs"]) == 3  # Including dir1, dir2, and subdir
    assert any(f.name == "file1.txt" for f in scan_results["files"])
    assert any(f.name == "file2.txt" for f in scan_results["files"])
    assert scan_results["total_size"] > 0

def test_build_directory_tree(tmp_path):
    """Test directory tree building functionality."""
    # Create test directory structure
    (tmp_path / "dir1").mkdir()
    (tmp_path / "dir1" / "file1.txt").write_text("content")
    (tmp_path / "dir2").mkdir()
    (tmp_path / "dir2" / "subdir").mkdir()
    (tmp_path / "dir2" / "subdir" / "file2.txt").write_text("content")
    
    tree = build_directory_tree(tmp_path)
    
    assert "dir1" in tree["children"]
    assert "dir2" in tree["children"]
    assert "subdir" in tree["children"]["dir2"]["children"]
    assert "file1.txt" in tree["children"]["dir1"]["children"]
    assert "file2.txt" in tree["children"]["dir2"]["children"]["subdir"]["children"]

def test_build_directory_tree_with_filters(tmp_path):
    """Test directory tree building with file filters."""
    # Create test files
    (tmp_path / "test.txt").write_text("content")
    (tmp_path / "test.jpg").write_bytes(b"image")
    (tmp_path / "test.py").write_text("print('hello')")
    
    # Test with extension filter
    tree = build_directory_tree(tmp_path, include_patterns=["*.txt", "*.py"])
    
    assert "test.txt" in tree["children"]
    assert "test.py" in tree["children"]
    assert "test.jpg" not in tree["children"] 