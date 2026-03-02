"""Tests for data models."""

import pytest
from datetime import datetime, timezone
from pathlib import Path
from pydantic import ValidationError
from src.core.models import (
    FileInfo,
    DirectoryStats,
    FileOperation,
    FileHash,
    CategoryConfig
)

class TestFileInfo:
    """Test suite for FileInfo model."""
    
    def test_valid_file_info(self):
        """Test creation of valid FileInfo instance."""
        now = datetime.now(timezone.utc)
        info = FileInfo(
            name="test.txt",
            path="/home/user/test.txt",
            size=1024,
            modified=now,
            is_dir=False,
            is_file=True,
            category="document"
        )
        assert info.name == "test.txt"
        assert info.path == "/home/user/test.txt"
        assert info.size == 1024
        assert info.modified == now
        assert info.is_dir is False
        assert info.is_file is True
        assert info.category == "document"

    def test_invalid_filename(self):
        """Test filename validation."""
        with pytest.raises(ValidationError) as exc_info:
            FileInfo(
                name="invalid/name.txt",
                path="/home/user/test.txt",
                size=1024,
                modified=datetime.now(timezone.utc),
                is_dir=False,
                is_file=True
            )
        error_dict = exc_info.value.errors()
        print("Invalid filename errors:", error_dict)
        assert any("contains path separators" in err["msg"] for err in error_dict)

        with pytest.raises(ValidationError) as exc_info:
            FileInfo(
                name="test*.txt",
                path="/home/user/test.txt",
                size=1024,
                modified=datetime.now(timezone.utc),
                is_dir=False,
                is_file=True
            )
        error_dict = exc_info.value.errors()
        print("Invalid filename chars errors:", error_dict)
        assert any("contains invalid characters" in err["msg"] for err in error_dict)

    def test_invalid_path(self):
        """Test path validation."""
        with pytest.raises(ValidationError) as exc_info:
            FileInfo(
                name="test.txt",
                path="../invalid/path",
                size=1024,
                modified=datetime.now(timezone.utc),
                is_dir=False,
                is_file=True
            )
        error_dict = exc_info.value.errors()
        print("Invalid path errors:", error_dict)
        assert any("invalid parent directory" in err["msg"].lower() for err in error_dict)

    def test_negative_size(self):
        """Test size validation."""
        with pytest.raises(ValidationError) as exc_info:
            FileInfo(
                name="test.txt",
                path="/home/user/test.txt",
                size=-1,
                modified=datetime.now(timezone.utc),
                is_dir=False,
                is_file=True
            )
        error_dict = exc_info.value.errors()
        assert any("greater than or equal to 0" in err["msg"] for err in error_dict)

class TestDirectoryStats:
    """Test suite for DirectoryStats model."""
    
    def test_valid_directory_stats(self):
        """Test creation of valid DirectoryStats instance."""
        stats = DirectoryStats(
            total_size=1048576,
            file_count=10,
            dir_count=2,
            extensions={".txt": 3, ".jpg": 5, ".pdf": 2},
            by_category={
                "documents": {"count": 5, "size": 512000},
                "images": {"count": 5, "size": 536576}
            }
        )
        assert stats.total_size == 1048576
        assert stats.file_count == 10
        assert stats.dir_count == 2
        assert stats.extensions[".txt"] == 3
        assert stats.by_category["documents"]["count"] == 5

    def test_extension_normalization(self):
        """Test extension case normalization."""
        stats = DirectoryStats(extensions={".TXT": 3, ".JPG": 5})
        assert ".txt" in stats.extensions
        assert ".jpg" in stats.extensions
        assert ".TXT" not in stats.extensions

    def test_negative_counts(self):
        """Test count validation."""
        with pytest.raises(ValidationError) as exc_info:
            DirectoryStats(total_size=-1)
        error_dict = exc_info.value.errors()
        assert any("greater than or equal to 0" in err["msg"] for err in error_dict)

        with pytest.raises(ValidationError) as exc_info:
            DirectoryStats(file_count=-1)
        error_dict = exc_info.value.errors()
        assert any("greater than or equal to 0" in err["msg"] for err in error_dict)

        with pytest.raises(ValidationError) as exc_info:
            DirectoryStats(dir_count=-1)
        error_dict = exc_info.value.errors()
        assert any("greater than or equal to 0" in err["msg"] for err in error_dict)

class TestFileOperation:
    """Test suite for FileOperation model."""
    
    def test_successful_operation(self):
        """Test successful operation result."""
        op = FileOperation(
            success=True,
            result="/path/to/file.txt"
        )
        assert op.success is True
        assert op.error_message is None
        assert op.result == "/path/to/file.txt"

    def test_failed_operation(self):
        """Test failed operation result."""
        op = FileOperation(
            success=False,
            error_message="File not found"
        )
        assert op.success is False
        assert op.error_message == "File not found"
        assert op.result is None

    def test_path_serialization(self):
        """Test Path object serialization."""
        path = Path("/path/to/file.txt")
        op = FileOperation(
            success=True,
            result=path
        )
        assert op.model_dump()["result"] == str(path)

class TestFileHash:
    """Test suite for FileHash model."""
    
    def test_valid_hash(self):
        """Test valid hash values."""
        algorithms = {
            "md5": "d41d8cd98f00b204e9800998ecf8427e",
            "sha1": "da39a3ee5e6b4b0d3255bfef95601890afd80709",
            "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "sha512": "cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e"
        }
        
        for algorithm, hash_value in algorithms.items():
            hash_info = FileHash(
                algorithm=algorithm,
                hash_value=hash_value,
                file_path="/path/to/file.txt"
            )
            assert hash_info.algorithm == algorithm
            assert hash_info.hash_value == hash_value

    def test_invalid_algorithm(self):
        """Test invalid hash algorithm."""
        with pytest.raises(ValidationError) as exc_info:
            FileHash(
                algorithm="invalid",
                hash_value="abcd",
                file_path="/path/to/file.txt"
            )
        error_dict = exc_info.value.errors()
        assert any("match pattern" in err["msg"] for err in error_dict)

    def test_invalid_hash_length(self):
        """Test invalid hash length."""
        with pytest.raises(ValidationError) as exc_info:
            FileHash(
                algorithm="sha256",
                hash_value="invalid",
                file_path="/path/to/file.txt"
            )
        error_dict = exc_info.value.errors()
        assert any("should have at least 32 characters" in err["msg"] for err in error_dict)

    def test_invalid_hash_characters(self):
        """Test invalid hash characters."""
        with pytest.raises(ValidationError) as exc_info:
            FileHash(
                algorithm="md5",
                hash_value="z" * 32,  # Invalid hex character
                file_path="/path/to/file.txt"
            )
        error_dict = exc_info.value.errors()
        assert any("hexadecimal characters" in err["msg"] for err in error_dict)

class TestCategoryConfig:
    """Test suite for CategoryConfig model."""
    
    def test_valid_category(self):
        """Test valid category configuration."""
        category = CategoryConfig(
            name="documents",
            extensions=[".pdf", "doc", ".txt"],
            description="Text-based document files"
        )
        assert category.name == "documents"
        assert set(category.extensions) == {".pdf", ".doc", ".txt"}
        assert category.description == "Text-based document files"

    def test_extension_normalization(self):
        """Test extension normalization."""
        category = CategoryConfig(
            name="images",
            extensions=["jpg", ".PNG", "JPEG"]
        )
        assert set(category.extensions) == {".jpg", ".png", ".jpeg"}

    def test_invalid_extension(self):
        """Test invalid extension format."""
        with pytest.raises(ValidationError) as exc_info:
            CategoryConfig(
                name="invalid",
                extensions=["..pdf", "doc/", "*txt"]
            )
        error_dict = exc_info.value.errors()
        assert any("Invalid file extension format" in err["msg"] for err in error_dict)

    def test_name_length(self):
        """Test category name length validation."""
        with pytest.raises(ValidationError) as exc_info:
            CategoryConfig(name="")
        error_dict = exc_info.value.errors()
        assert any("at least 1 character" in err["msg"] for err in error_dict)

        with pytest.raises(ValidationError) as exc_info:
            CategoryConfig(name="a" * 51)
        error_dict = exc_info.value.errors()
        assert any("at most 50 characters" in err["msg"] for err in error_dict)

    def test_description_length(self):
        """Test description length validation."""
        with pytest.raises(ValidationError) as exc_info:
            CategoryConfig(
                name="test",
                description="a" * 501
            )
        error_dict = exc_info.value.errors()
        assert any("at most 200 characters" in err["msg"] for err in error_dict)


class TestFileInfoEdgeCases:
    """Additional edge case tests for FileInfo model."""

    def test_model_dump_serializes_datetime(self):
        """Test that model_dump converts datetime to ISO format."""
        now = datetime.now(timezone.utc)
        info = FileInfo(
            name="test.txt",
            path="/home/user/test.txt",
            size=100,
            modified=now,
            is_dir=False,
            is_file=True,
        )
        dumped = info.model_dump()
        assert isinstance(dumped["modified"], str)

    def test_path_normalized(self):
        """Test that paths are normalized."""
        info = FileInfo(
            name="test.txt",
            path="/home/user/./docs/../test.txt",
            size=100,
            modified=datetime.now(timezone.utc),
            is_dir=False,
            is_file=True,
        )
        assert ".." not in info.path

    def test_relative_path_rejected(self):
        """Test that relative paths are rejected."""
        with pytest.raises(ValidationError):
            FileInfo(
                name="test.txt",
                path="relative/path/test.txt",
                size=100,
                modified=datetime.now(timezone.utc),
                is_dir=False,
                is_file=True,
            )

    def test_empty_name_rejected(self):
        """Test that empty names are rejected."""
        with pytest.raises(ValidationError):
            FileInfo(
                name="",
                path="/home/user/test.txt",
                size=0,
                modified=datetime.now(timezone.utc),
                is_dir=False,
                is_file=True,
            )

    def test_whitespace_name_rejected(self):
        """Test that names with leading/trailing whitespace are rejected."""
        with pytest.raises(ValidationError):
            FileInfo(
                name=" test.txt ",
                path="/home/user/test.txt",
                size=0,
                modified=datetime.now(timezone.utc),
                is_dir=False,
                is_file=True,
            )


class TestFileOperationEdgeCases:
    """Additional tests for FileOperation model."""

    def test_path_serialization_in_model_dump(self):
        """Test that Path objects are serialized in model_dump."""
        from pathlib import Path as P

        op = FileOperation(success=True, result=P("/some/path"))
        dumped = op.model_dump()
        assert dumped["result"] == "/some/path"


class TestFileHashEdgeCases:
    """Additional edge case tests for FileHash."""

    def test_hash_length_mismatch_for_sha256(self):
        """Test that wrong-length hash for sha256 is rejected."""
        with pytest.raises(ValidationError):
            FileHash(
                algorithm="sha256",
                hash_value="abcdef1234567890" * 2,  # 32 chars, needs 64
                file_path="/path/to/file.txt",
            )


class TestCategoryConfigEdgeCases:
    """Additional edge case tests for CategoryConfig."""

    def test_non_list_extensions_rejected(self):
        """Test that non-list extensions value is rejected."""
        with pytest.raises(ValidationError):
            CategoryConfig(
                name="test",
                extensions="not a list",
            )

    def test_non_string_extension_in_list_rejected(self):
        """Test that non-string items in extensions list are rejected."""
        with pytest.raises(ValidationError):
            CategoryConfig(
                name="test",
                extensions=[123, 456],
            )


class TestFileOperationModelDumpPath:
    """Test FileOperation.model_dump with Path objects."""

    def test_model_dump_does_not_contain_path_object(self):
        """Test model_dump serializes any remaining Path objects."""
        # The field_validator already converts Path to str,
        # but model_dump has a fallback check
        op = FileOperation(success=True, result="/some/path")
        dumped = op.model_dump()
        assert isinstance(dumped["result"], str)