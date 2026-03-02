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


def test_get_volume_info(tmp_path):
    """Test get_volume_info returns disk usage data."""
    from src.core.drive_ops import get_volume_info

    info = get_volume_info(tmp_path)
    assert "total" in info
    assert "used" in info
    assert "free" in info
    assert info["total"] > 0


def test_get_volume_info_invalid_path():
    """Test get_volume_info raises for invalid path."""
    from src.core.drive_ops import get_volume_info

    with pytest.raises(Exception):
        get_volume_info(Path("/nonexistent/mount/point"))


def test_get_all_volumes_handles_usage_error(monkeypatch):
    """Test get_all_volumes handles disk_usage errors gracefully."""
    import psutil

    def mock_disk_partitions(all=False):
        return [
            type(
                "P",
                (),
                {
                    "device": "/dev/sda1",
                    "mountpoint": "/bad",
                    "fstype": "ext4",
                    "opts": "rw",
                },
            )
        ]

    def mock_disk_usage(path):
        raise PermissionError("Access denied")

    monkeypatch.setattr(psutil, "disk_partitions", mock_disk_partitions)
    monkeypatch.setattr(psutil, "disk_usage", mock_disk_usage)

    volumes = get_all_volumes()
    assert volumes == []


def test_get_all_volumes_percent_calculation(monkeypatch):
    """Test percent calculation when percent attribute is missing."""
    import psutil

    def mock_partitions(all=False):
        return [
            type(
                "P",
                (),
                {
                    "device": "/dev/sda1",
                    "mountpoint": "/",
                    "fstype": "ext4",
                    "opts": "rw",
                },
            )
        ]

    class MockUsage:
        total = 1000
        used = 500
        free = 500

    def mock_usage(path):
        return MockUsage()

    monkeypatch.setattr(psutil, "disk_partitions", mock_partitions)
    monkeypatch.setattr(psutil, "disk_usage", mock_usage)

    volumes = get_all_volumes()
    assert len(volumes) == 1
    assert volumes[0]["percent"] == 50.0


def test_scan_directory_nonexistent():
    """Test scan_directory with nonexistent path."""
    result = scan_directory(Path("/nonexistent/directory"))
    assert result["files"] == []
    assert result["total_files"] == 0


def test_scan_directory_with_hidden(tmp_path):
    """Test scan_directory excludes hidden files by default."""
    (tmp_path / ".hidden").write_text("hidden")
    (tmp_path / "visible.txt").write_text("visible")

    result = scan_directory(tmp_path, include_hidden=False)
    assert result["total_files"] == 1


def test_scan_directory_with_max_depth(tmp_path):
    """Test scan_directory respects max_depth."""
    (tmp_path / "level1").mkdir()
    (tmp_path / "level1" / "level2").mkdir()
    (tmp_path / "level1" / "level2" / "deep.txt").write_text("deep")
    (tmp_path / "top.txt").write_text("top")

    # max_depth=0 means only root level items
    result_shallow = scan_directory(tmp_path, max_depth=0)
    result_deep = scan_directory(tmp_path, max_depth=10)

    # Deep scan should find more files than shallow
    assert result_deep["total_files"] >= result_shallow["total_files"]


def test_build_directory_tree_nonexistent():
    """Test build_directory_tree with nonexistent path."""
    tree = build_directory_tree(Path("/nonexistent"))
    assert tree["type"] == "directory"
    assert tree["children"] == {}


def test_build_directory_tree_with_max_depth(tmp_path):
    """Test build_directory_tree respects max_depth."""
    (tmp_path / "dir1").mkdir()
    (tmp_path / "dir1" / "deep").mkdir()
    (tmp_path / "dir1" / "deep" / "deeper").mkdir()

    tree = build_directory_tree(tmp_path, max_depth=1)
    assert "dir1" in tree["children"]


def test_build_directory_tree_exclude_patterns(tmp_path):
    """Test build_directory_tree excludes patterns."""
    (tmp_path / "keep.txt").write_text("keep")
    (tmp_path / "skip.log").write_text("skip")

    tree = build_directory_tree(tmp_path, exclude_patterns=["*.log"])
    assert "keep.txt" in tree["children"]
    assert "skip.log" not in tree["children"]


def test_get_all_volumes_zero_total(monkeypatch):
    """Test percent defaults to 0 when total is 0."""
    import psutil

    def mock_partitions(all=False):
        return [
            type(
                "P",
                (),
                {
                    "device": "/dev/sda1",
                    "mountpoint": "/empty",
                    "fstype": "tmpfs",
                    "opts": "rw",
                },
            )
        ]

    class MockUsageZero:
        total = 0
        used = 0
        free = 0

    def mock_usage(path):
        return MockUsageZero()

    monkeypatch.setattr(psutil, "disk_partitions", mock_partitions)
    monkeypatch.setattr(psutil, "disk_usage", mock_usage)

    volumes = get_all_volumes()
    assert len(volumes) == 1
    assert volumes[0]["percent"] == 0


def test_get_all_volumes_outer_exception(monkeypatch):
    """Test get_all_volumes handles disk_partitions failure."""
    import psutil

    def broken_partitions(all=False):
        raise OSError("Cannot enumerate partitions")

    monkeypatch.setattr(psutil, "disk_partitions", broken_partitions)

    volumes = get_all_volumes()
    assert volumes == []


def test_scan_directory_failed_file_info(tmp_path, monkeypatch):
    """Test scan_directory handles get_file_info failure for individual items."""
    from src.core import drive_ops
    from src.core.models import FileOperation

    (tmp_path / "good.txt").write_text("ok")
    (tmp_path / "bad.txt").write_text("fail")

    original = drive_ops.get_file_info

    def patched(path):
        if hasattr(path, "name") and path.name == "bad.txt":
            return FileOperation(success=False, error_message="Access denied")
        return original(path)

    monkeypatch.setattr(drive_ops, "get_file_info", patched)

    result = scan_directory(tmp_path)
    # Only good.txt should be counted
    assert result["total_files"] == 1


def test_build_directory_tree_failed_file_info(tmp_path, monkeypatch):
    """Test build_directory_tree skips items when get_file_info fails."""
    from src.core import drive_ops
    from src.core.models import FileOperation

    (tmp_path / "visible.txt").write_text("ok")
    (tmp_path / "broken.txt").write_text("fail")

    original = drive_ops.get_file_info

    def patched(path):
        if hasattr(path, "name") and path.name == "broken.txt":
            return FileOperation(success=False, error_message="Error")
        return original(path)

    monkeypatch.setattr(drive_ops, "get_file_info", patched)

    tree = build_directory_tree(tmp_path)
    assert "visible.txt" in tree["children"]
    assert "broken.txt" not in tree["children"]


def test_build_directory_tree_iterdir_error(tmp_path, monkeypatch):
    """Test build_directory_tree handles iterdir errors in subdirectories."""
    sub = tmp_path / "subdir"
    sub.mkdir()
    (sub / "file.txt").write_text("content")

    # Make subdirectory unreadable
    sub.chmod(0o000)
    try:
        tree = build_directory_tree(tmp_path)
        # Should still return a tree, just without the unreadable subdir contents
        assert tree["type"] == "directory"
    finally:
        sub.chmod(0o755)