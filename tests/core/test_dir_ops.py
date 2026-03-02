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


def test_ensure_master_folders_with_config(tmp_path, monkeypatch):
    """Test master folder creation using config categories."""
    import json
    from src.config import settings

    config = {
        **settings.DEFAULT_CONFIG,
        "master_folder_root": str(tmp_path / "master"),
    }
    config_file = tmp_path / ".efm_config.json"
    config_file.write_text(json.dumps(config))
    monkeypatch.setattr(settings, "CONFIG_FILE", config_file)

    result = ensure_master_folders()
    assert (tmp_path / "master").is_dir()
    assert len(result) > 0


def test_analyze_directory_with_hidden_files(tmp_path):
    """Test that hidden files are excluded by default."""
    (tmp_path / ".hidden_file").write_text("hidden")
    (tmp_path / "visible.txt").write_text("visible")

    stats = analyze_directory(tmp_path)
    assert stats["file_count"] == 1


def test_analyze_directory_includes_hidden(tmp_path):
    """Test that hidden files can be included."""
    (tmp_path / ".hidden_file").write_text("hidden")
    (tmp_path / "visible.txt").write_text("visible")

    stats = analyze_directory(tmp_path, include_hidden=True)
    assert stats["file_count"] == 2


def test_organize_files_copy_mode(tmp_path):
    """Test organizing files in copy mode (not move)."""
    source = tmp_path / "source"
    source.mkdir()
    (source / "test.txt").write_text("content")

    dest = tmp_path / "dest"
    dest.mkdir()

    organize_files(source, dest, move_files=False)

    # Source file should still exist (copy, not move)
    assert (source / "test.txt").exists()
    assert (dest / "Documents" / "test.txt").exists()


def test_organize_files_with_copy_suffix_in_name(tmp_path):
    """Test organizing files that already have (copy N) in name."""
    source = tmp_path / "source"
    source.mkdir()

    dest = tmp_path / "dest"
    dest.mkdir()
    doc_dir = dest / "Documents"
    doc_dir.mkdir()

    # Create a file that will collide
    (doc_dir / "test.txt").write_text("existing")
    (source / "test.txt").write_text("new content")

    organize_files(source, dest)

    files = list(doc_dir.glob("*.txt"))
    assert len(files) == 2


def test_ensure_master_folders_raises_on_bad_path(tmp_path):
    """Test ensure_master_folders propagates exception for unwritable path."""
    # Use a file path as root to trigger OSError
    blocker = tmp_path / "blocker"
    blocker.write_text("I am a file")
    bad_root = blocker / "subdir"

    with pytest.raises(Exception):
        ensure_master_folders(bad_root)


def test_organize_files_skips_directories(tmp_path):
    """Test that organize_files skips directories in source."""
    source = tmp_path / "source"
    source.mkdir()
    (source / "subdir").mkdir()
    (source / "subdir" / "nested.txt").write_text("nested")
    (source / "top.txt").write_text("top level")

    dest = tmp_path / "dest"
    dest.mkdir()

    counts = organize_files(source, dest)
    # Both files should be organized (rglob finds nested files)
    total = sum(counts.values())
    assert total == 2


def test_organize_files_strips_copy_suffix_on_collision(tmp_path):
    """Test that files with existing '(copy N)' suffix get properly renamed."""
    source = tmp_path / "source"
    source.mkdir()

    dest = tmp_path / "dest"
    dest.mkdir()
    doc_dir = dest / "Documents"
    doc_dir.mkdir()

    # Pre-populate dest with original and first copy
    (doc_dir / "report.txt").write_text("original")
    (doc_dir / "report (copy 1).txt").write_text("copy 1")

    # Source has a file named with copy suffix that will collide
    (source / "report (copy 1).txt").write_text("new copy 1")

    organize_files(source, dest)

    files = list(doc_dir.glob("report*.txt"))
    assert len(files) == 3


def test_organize_files_handles_move_error(tmp_path, monkeypatch):
    """Test organize_files handles error when moving individual files."""
    import shutil

    source = tmp_path / "source"
    source.mkdir()
    (source / "test.txt").write_text("content")

    dest = tmp_path / "dest"
    dest.mkdir()

    original_move = shutil.move

    def broken_move(src, dst):
        raise PermissionError("Cannot move file")

    monkeypatch.setattr(shutil, "move", broken_move)

    # Should not raise - errors are caught per-file
    counts = organize_files(source, dest)
    assert sum(counts.values()) == 0


def test_organize_files_outer_exception(monkeypatch):
    """Test organize_files raises on outer exception."""
    from src.core import dir_ops

    bad_source = Path("/nonexistent/source")

    # Monkeypatch ensure_master_folders to raise
    def bad_ensure(p):
        raise RuntimeError("cannot create folders")

    monkeypatch.setattr(dir_ops, "ensure_master_folders", bad_ensure)

    with pytest.raises(RuntimeError):
        organize_files(bad_source, Path("/tmp/dest"))


def test_analyze_directory_with_unreadable_file(tmp_path, monkeypatch):
    """Test analyze_directory handles get_file_info failure gracefully."""
    from src.core import dir_ops
    from src.core.models import FileOperation

    (tmp_path / "good.txt").write_text("readable")
    (tmp_path / "bad.txt").write_text("unreadable")

    original_get_file_info = dir_ops.get_file_info

    def patched_get_file_info(path):
        if hasattr(path, 'name') and path.name == "bad.txt":
            return FileOperation(success=False, error_message="Permission denied")
        return original_get_file_info(path)

    monkeypatch.setattr(dir_ops, "get_file_info", patched_get_file_info)

    stats = analyze_directory(tmp_path)
    # Only good.txt should be counted
    assert stats["file_count"] == 1