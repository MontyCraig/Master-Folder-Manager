"""
Data models for Enhanced Folder Manager.

This module contains Pydantic models for data validation and serialization.
"""

from datetime import datetime
from typing import Dict, List, Optional, Union, Any
from pathlib import Path
from pydantic import BaseModel, Field, field_validator, ConfigDict, model_validator
import os
import re

class FileInfo(BaseModel):
    """Model for file information with strict validation."""
    name: str = Field(
        ..., 
        description="Name of the file",
        examples=["document.txt", "image.jpg"],
        min_length=1,
        max_length=255
    )
    path: str = Field(
        ..., 
        description="Full path to the file",
        examples=["/home/user/documents/file.txt"]
    )
    size: int = Field(
        ..., 
        description="Size of the file in bytes",
        examples=[1024, 2048],
        ge=0
    )
    modified: datetime = Field(
        ..., 
        description="Last modification timestamp"
    )
    is_dir: bool = Field(
        ..., 
        description="Whether the item is a directory"
    )
    is_file: bool = Field(
        ..., 
        description="Whether the item is a file"
    )
    category: Optional[str] = Field(
        None, 
        description="File category if applicable",
        examples=["document", "image", "video"]
    )

    @field_validator('path')
    @classmethod
    def validate_path(cls, v: str) -> str:
        """Validate and sanitize file path."""
        # Normalize path separators and remove any potential directory traversal
        clean_path = os.path.normpath(v)
        if '..' in clean_path:
            raise ValueError("Path contains invalid parent directory references")
        if not os.path.isabs(clean_path):
            raise ValueError("Path must be absolute")
        return clean_path

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate filename."""
        if not v or v.strip() != v:
            raise ValueError("Invalid filename: must not be empty or contain leading/trailing whitespace")
        if os.path.sep in v or (os.path.altsep and os.path.altsep in v):
            raise ValueError("Filename contains path separators")
        if re.search(r'[<>:"|?*]', v):
            raise ValueError("Filename contains invalid characters")
        return v

    def model_dump(self, **kwargs):
        """Custom serialization for datetime and Path objects."""
        data = super().model_dump(**kwargs)
        if isinstance(data.get('modified'), datetime):
            data['modified'] = data['modified'].isoformat()
        return data

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "document.txt",
                "path": "/home/user/documents/document.txt",
                "size": 1024,
                "modified": "2024-04-08T12:00:00",
                "is_dir": False,
                "is_file": True,
                "category": "document"
            }
        }
    )

class DirectoryStats(BaseModel):
    """Model for directory analysis results with validation."""
    total_size: int = Field(
        0, 
        description="Total size of all files in bytes",
        ge=0
    )
    file_count: int = Field(
        0, 
        description="Number of files",
        ge=0
    )
    dir_count: int = Field(
        0, 
        description="Number of directories",
        ge=0
    )
    extensions: Dict[str, int] = Field(
        default_factory=dict,
        description="Count of file extensions"
    )
    by_category: Dict[str, Dict[str, int]] = Field(
        default_factory=dict,
        description="Files grouped by category"
    )

    @field_validator('extensions')
    @classmethod
    def validate_extensions(cls, v: Dict[str, int]) -> Dict[str, int]:
        """Validate extension counts."""
        return {ext.lower(): count for ext, count in v.items()}

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total_size": 1048576,
                "file_count": 10,
                "dir_count": 2,
                "extensions": {".txt": 3, ".jpg": 5, ".pdf": 2},
                "by_category": {
                    "documents": {"count": 5, "size": 512000},
                    "images": {"count": 5, "size": 536576}
                }
            }
        }
    )

class FileOperation(BaseModel):
    """Model for file operation results with error handling."""
    success: bool = Field(
        ..., 
        description="Whether the operation was successful"
    )
    error_message: Optional[str] = Field(
        None, 
        description="Error message if operation failed"
    )
    result: Optional[Union[str, Path, Dict[str, Any], FileInfo, bool]] = Field(
        None,
        description="Operation result data"
    )

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator('result')
    @classmethod
    def serialize_path(cls, v: Optional[Union[str, Path, Dict[str, Any], FileInfo, bool]]) -> Optional[Union[str, Dict[str, Any], FileInfo, bool]]:
        """Convert Path objects to strings in the result field."""
        if isinstance(v, Path):
            return str(v)
        return v

    def model_dump(self, **kwargs):
        """Custom serialization to handle Path objects."""
        data = super().model_dump(**kwargs)
        if isinstance(data.get('result'), Path):
            data['result'] = str(data['result'])
        return data

class FileHash(BaseModel):
    """Model for file hash results with algorithm validation."""
    algorithm: str = Field(
        ..., 
        description="Hash algorithm used",
        pattern='^(md5|sha1|sha256|sha512)$'
    )
    hash_value: str = Field(
        ..., 
        description="Computed hash value",
        min_length=32,
        max_length=128
    )
    file_path: str = Field(
        ..., 
        description="Path of the hashed file"
    )

    @field_validator('algorithm')
    @classmethod
    def validate_algorithm(cls, v: str) -> str:
        """Validate hash algorithm."""
        return v.lower()

    @field_validator('hash_value')
    @classmethod
    def validate_hash(cls, v: str, info) -> str:
        """Validate hash value format."""
        algorithm = info.data.get('algorithm')
        if algorithm:
            expected_length = {
                'md5': 32,
                'sha1': 40,
                'sha256': 64,
                'sha512': 128
            }[algorithm]
            if len(v) != expected_length:
                raise ValueError(
                    f"Hash length mismatch for {algorithm}: "
                    f"expected {expected_length}, got {len(v)}"
                )
        if not re.match(r'^[a-fA-F0-9]+$', v):
            raise ValueError("Hash value must contain only hexadecimal characters")
        return v.lower()

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "algorithm": "sha256",
                "hash_value": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                "file_path": "/path/to/file.txt"
            }
        }
    )

class CategoryConfig(BaseModel):
    """Model for file category configuration with validation."""
    name: str = Field(
        ..., 
        description="Category name",
        min_length=1,
        max_length=50
    )
    extensions: List[str] = Field(
        default_factory=list,
        description="File extensions for this category"
    )
    description: Optional[str] = Field(
        None, 
        description="Category description",
        max_length=200
    )

    @field_validator('extensions', mode='before')
    @classmethod
    def validate_extension(cls, v: List[str]) -> List[str]:
        """Validate file extension."""
        if not isinstance(v, list):
            raise ValueError("Extensions must be a list")
        normalized = []
        for ext in v:
            if not isinstance(ext, str):
                raise ValueError("Extension must be a string")
            ext = ext.lower()
            if not ext.startswith('.'):
                ext = '.' + ext
            if not re.match(r'^\.[a-z0-9]+$', ext):
                raise ValueError("Invalid file extension format")
            normalized.append(ext)
        return normalized

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "documents",
                "extensions": [".pdf", ".doc", ".txt"],
                "description": "Text-based document files"
            }
        }
    ) 