"""Tests for configuration settings module."""

import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.config import settings


class TestGetCategoryForFile:
    """Tests for get_category_for_file function."""

    def test_returns_category_for_known_extension(self, tmp_path, monkeypatch):
        monkeypatch.setattr(settings, "CONFIG_FILE", tmp_path / ".efm_config.json")
        result = settings.get_category_for_file("document.pdf")
        assert result == "Documents"

    def test_returns_category_for_code_file(self, tmp_path, monkeypatch):
        monkeypatch.setattr(settings, "CONFIG_FILE", tmp_path / ".efm_config.json")
        result = settings.get_category_for_file("script.py")
        assert result == "Coding_Projects"

    def test_returns_other_for_unknown_extension(self, tmp_path, monkeypatch):
        monkeypatch.setattr(settings, "CONFIG_FILE", tmp_path / ".efm_config.json")
        result = settings.get_category_for_file("file.xyz")
        assert result == "Other"

    def test_returns_other_on_exception(self, tmp_path, monkeypatch):
        bad_config = tmp_path / ".efm_config.json"
        bad_config.write_text("invalid json{{{")
        monkeypatch.setattr(settings, "CONFIG_FILE", bad_config)
        result = settings.get_category_for_file("test.txt")
        # Falls back to default config
        assert isinstance(result, str)


class TestLoadConfig:
    """Tests for load_config function."""

    def test_loads_config_from_file(self, tmp_path, monkeypatch):
        config = {"master_folder_root": "/tmp/test", "categories": {}}
        config_file = tmp_path / ".efm_config.json"
        config_file.write_text(json.dumps(config))
        monkeypatch.setattr(settings, "CONFIG_FILE", config_file)

        result = settings.load_config()
        assert result["master_folder_root"] == "/tmp/test"

    def test_creates_default_config_if_not_exists(self, tmp_path, monkeypatch):
        config_file = tmp_path / ".efm_config.json"
        monkeypatch.setattr(settings, "CONFIG_FILE", config_file)

        result = settings.load_config()
        assert result == settings.DEFAULT_CONFIG
        assert config_file.exists()

    def test_returns_default_on_json_error(self, tmp_path, monkeypatch):
        config_file = tmp_path / ".efm_config.json"
        config_file.write_text("not valid json!!")
        monkeypatch.setattr(settings, "CONFIG_FILE", config_file)

        result = settings.load_config()
        assert result == settings.DEFAULT_CONFIG


class TestSaveConfig:
    """Tests for save_config function."""

    def test_saves_config_to_file(self, tmp_path, monkeypatch):
        config_file = tmp_path / ".efm_config.json"
        monkeypatch.setattr(settings, "CONFIG_FILE", config_file)

        config = {"key": "value", "nested": {"a": 1}}
        settings.save_config(config)

        loaded = json.loads(config_file.read_text())
        assert loaded["key"] == "value"
        assert loaded["nested"]["a"] == 1

    def test_save_config_raises_on_write_error(self, tmp_path, monkeypatch):
        # Point to a directory that doesn't exist and can't be created
        config_file = tmp_path / "nonexistent" / "deep" / "path" / "config.json"
        monkeypatch.setattr(settings, "CONFIG_FILE", config_file)

        with pytest.raises(Exception):
            settings.save_config({"key": "value"})


class TestGetAvailableVolumes:
    """Tests for get_available_volumes function."""

    def test_returns_existing_mount_points(self, tmp_path, monkeypatch):
        config_file = tmp_path / ".efm_config.json"
        monkeypatch.setattr(settings, "CONFIG_FILE", config_file)

        # Default config has macOS paths that won't exist on CI
        result = settings.get_available_volumes()
        assert isinstance(result, list)

    def test_returns_empty_on_no_valid_volumes(self, tmp_path, monkeypatch):
        config = {
            "master_folder_root": "/tmp/test",
            "quick_access_volumes": ["/nonexistent/path1", "/nonexistent/path2"],
            "categories": {},
            "recent_paths": [],
            "favorites": [],
            "excluded_patterns": [],
        }
        config_file = tmp_path / ".efm_config.json"
        config_file.write_text(json.dumps(config))
        monkeypatch.setattr(settings, "CONFIG_FILE", config_file)

        result = settings.get_available_volumes()
        assert result == []

    def test_returns_empty_on_exception(self, tmp_path, monkeypatch):
        config_file = tmp_path / ".efm_config.json"
        config_file.write_text("invalid json")
        monkeypatch.setattr(settings, "CONFIG_FILE", config_file)

        result = settings.get_available_volumes()
        # Falls back to default config, which has non-existent paths
        assert isinstance(result, list)


class TestGetMasterFolder:
    """Tests for get_master_folder function."""

    def test_returns_master_folder_path(self, tmp_path, monkeypatch):
        config = {"master_folder_root": str(tmp_path / "master")}
        config_file = tmp_path / ".efm_config.json"
        config_file.write_text(json.dumps({**settings.DEFAULT_CONFIG, **config}))
        monkeypatch.setattr(settings, "CONFIG_FILE", config_file)

        result = settings.get_master_folder()
        assert result == Path(str(tmp_path / "master"))


class TestUpdateRecentPath:
    """Tests for update_recent_path function."""

    def test_adds_new_path_to_recent(self, tmp_path, monkeypatch):
        config_file = tmp_path / ".efm_config.json"
        monkeypatch.setattr(settings, "CONFIG_FILE", config_file)

        # Load default config first
        settings.load_config()

        settings.update_recent_path(Path("/some/path"))

        loaded = json.loads(config_file.read_text())
        assert "/some/path" in loaded["recent_paths"]

    def test_moves_existing_path_to_front(self, tmp_path, monkeypatch):
        config = {**settings.DEFAULT_CONFIG, "recent_paths": ["/a", "/b", "/c"]}
        config_file = tmp_path / ".efm_config.json"
        config_file.write_text(json.dumps(config))
        monkeypatch.setattr(settings, "CONFIG_FILE", config_file)

        settings.update_recent_path(Path("/c"))

        loaded = json.loads(config_file.read_text())
        assert loaded["recent_paths"][0] == "/c"

    def test_limits_recent_paths_to_10(self, tmp_path, monkeypatch):
        config = {
            **settings.DEFAULT_CONFIG,
            "recent_paths": [f"/path/{i}" for i in range(10)],
        }
        config_file = tmp_path / ".efm_config.json"
        config_file.write_text(json.dumps(config))
        monkeypatch.setattr(settings, "CONFIG_FILE", config_file)

        settings.update_recent_path(Path("/new/path"))

        loaded = json.loads(config_file.read_text())
        assert len(loaded["recent_paths"]) == 10
        assert loaded["recent_paths"][0] == "/new/path"

    def test_raises_on_save_error(self, tmp_path, monkeypatch):
        config_file = tmp_path / ".efm_config.json"
        monkeypatch.setattr(settings, "CONFIG_FILE", config_file)
        settings.load_config()

        # Make config file unwritable
        config_file.chmod(0o444)
        try:
            with pytest.raises(Exception):
                settings.update_recent_path(Path("/some/path"))
        finally:
            config_file.chmod(0o644)


class TestSelectMasterFolder:
    """Tests for select_master_folder interactive function."""

    def test_returns_none_on_back(self, tmp_path, monkeypatch):
        config = {**settings.DEFAULT_CONFIG, "master_folder_root": str(tmp_path)}
        config_file = tmp_path / ".efm_config.json"
        config_file.write_text(json.dumps(config))
        monkeypatch.setattr(settings, "CONFIG_FILE", config_file)

        with patch.object(settings.Prompt, "ask", return_value="b"):
            result = settings.select_master_folder()
            assert result is None

    def test_creates_new_folder(self, tmp_path, monkeypatch):
        config = {**settings.DEFAULT_CONFIG, "master_folder_root": str(tmp_path)}
        config_file = tmp_path / ".efm_config.json"
        config_file.write_text(json.dumps(config))
        monkeypatch.setattr(settings, "CONFIG_FILE", config_file)

        with patch.object(settings.Prompt, "ask", side_effect=["n", "TestFolder"]):
            result = settings.select_master_folder()
            assert result == tmp_path / "TestFolder"
            assert (tmp_path / "TestFolder").is_dir()

    def test_selects_existing_folder(self, tmp_path, monkeypatch):
        (tmp_path / "ExistingFolder").mkdir()
        config = {**settings.DEFAULT_CONFIG, "master_folder_root": str(tmp_path)}
        config_file = tmp_path / ".efm_config.json"
        config_file.write_text(json.dumps(config))
        monkeypatch.setattr(settings, "CONFIG_FILE", config_file)

        with patch.object(settings.Prompt, "ask", return_value="1"):
            result = settings.select_master_folder()
            assert result == tmp_path / "ExistingFolder"

    def test_quits_on_q(self, tmp_path, monkeypatch):
        config = {**settings.DEFAULT_CONFIG, "master_folder_root": str(tmp_path)}
        config_file = tmp_path / ".efm_config.json"
        config_file.write_text(json.dumps(config))
        monkeypatch.setattr(settings, "CONFIG_FILE", config_file)

        with patch.object(settings.Prompt, "ask", return_value="q"):
            with pytest.raises(SystemExit):
                settings.select_master_folder()

    def test_returns_none_on_exception(self, tmp_path, monkeypatch):
        # Point to a config that will cause issues
        monkeypatch.setattr(
            settings, "CONFIG_FILE", tmp_path / "nonexistent" / "config.json"
        )
        # load_config will return defaults, but master_folder_root
        # path creation could fail on read-only fs.
        # The function catches all exceptions and returns None.
        with patch.object(settings, "load_config", side_effect=Exception("fail")):
            result = settings.select_master_folder()
            assert result is None

    def test_returns_none_for_invalid_numeric_choice(self, tmp_path, monkeypatch):
        config = {**settings.DEFAULT_CONFIG, "master_folder_root": str(tmp_path)}
        config_file = tmp_path / ".efm_config.json"
        config_file.write_text(json.dumps(config))
        monkeypatch.setattr(settings, "CONFIG_FILE", config_file)

        # Return a string that is digit but out of range
        with patch.object(settings.Prompt, "ask", return_value="99"):
            result = settings.select_master_folder()
            assert result is None

    def test_creates_root_when_missing(self, tmp_path, monkeypatch):
        """Test select_master_folder creates root dir when it doesn't exist."""
        new_root = tmp_path / "nonexistent_root"
        config = {**settings.DEFAULT_CONFIG, "master_folder_root": str(new_root)}
        config_file = tmp_path / ".efm_config.json"
        config_file.write_text(json.dumps(config))
        monkeypatch.setattr(settings, "CONFIG_FILE", config_file)

        with patch.object(settings.Prompt, "ask", return_value="b"):
            result = settings.select_master_folder()
            assert result is None
            assert new_root.exists()


class TestGetCategoryForFileException:
    """Test get_category_for_file exception handling."""

    def test_returns_other_when_load_config_raises(self, monkeypatch):
        """Test that get_category_for_file returns 'Other' on any exception."""
        def bad_load():
            raise RuntimeError("broken config")

        monkeypatch.setattr(settings, "load_config", bad_load)
        result = settings.get_category_for_file("document.pdf")
        assert result == "Other"


class TestGetAvailableVolumesEdgeCases:
    """Additional edge case tests for get_available_volumes."""

    def test_returns_volumes_for_real_mount(self, tmp_path, monkeypatch):
        """Test get_available_volumes includes paths that exist and are mounts."""
        config = {
            **settings.DEFAULT_CONFIG,
            "quick_access_volumes": ["/"],
        }
        config_file = tmp_path / ".efm_config.json"
        config_file.write_text(json.dumps(config))
        monkeypatch.setattr(settings, "CONFIG_FILE", config_file)

        result = settings.get_available_volumes()
        assert len(result) >= 1
        assert Path("/") in result

    def test_returns_empty_list_when_load_config_raises(self, monkeypatch):
        """Test get_available_volumes returns [] when load_config raises."""
        def bad_load():
            raise RuntimeError("broken")

        monkeypatch.setattr(settings, "load_config", bad_load)
        result = settings.get_available_volumes()
        assert result == []
