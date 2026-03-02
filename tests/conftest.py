"""Shared test fixtures for Master Folder Manager."""

import pytest
from pathlib import Path
from datetime import datetime, timezone


@pytest.fixture
def sample_file(tmp_path):
    """Create a sample text file for testing."""
    f = tmp_path / "sample.txt"
    f.write_text("sample content")
    return f


@pytest.fixture
def sample_dir(tmp_path):
    """Create a populated directory structure for testing."""
    # Create subdirectories
    (tmp_path / "docs").mkdir()
    (tmp_path / "images").mkdir()
    (tmp_path / "code").mkdir()

    # Create files in various categories
    (tmp_path / "docs" / "readme.txt").write_text("readme content")
    (tmp_path / "docs" / "notes.pdf").write_bytes(b"fake pdf")
    (tmp_path / "images" / "photo.jpg").write_bytes(b"fake jpeg")
    (tmp_path / "images" / "icon.png").write_bytes(b"fake png")
    (tmp_path / "code" / "app.py").write_text("print('hello')")
    (tmp_path / "code" / "util.js").write_text("console.log('hi')")
    (tmp_path / "archive.zip").write_bytes(b"fake zip")

    return tmp_path


@pytest.fixture
def config_file(tmp_path):
    """Create a temporary config file."""
    import json

    config = {
        "master_folder_root": str(tmp_path / "master"),
        "quick_access_volumes": [str(tmp_path)],
        "categories": {
            "Documents": {
                "extensions": [".txt", ".pdf", ".doc"],
                "priority": 1,
            },
            "Images": {
                "extensions": [".jpg", ".png", ".gif"],
                "priority": 2,
            },
            "Code": {
                "extensions": [".py", ".js", ".java"],
                "priority": 3,
            },
        },
        "recent_paths": [],
        "favorites": [],
        "excluded_patterns": [".git", "__pycache__"],
    }

    config_path = tmp_path / ".efm_config.json"
    config_path.write_text(json.dumps(config, indent=4))
    return config_path, config


@pytest.fixture
def now():
    """Return a timezone-aware UTC datetime."""
    return datetime.now(timezone.utc)
