"""
Data models for Enhanced Folder Manager.

This module contains Pydantic models for data validation and serialization.
"""

from datetime import datetime
from typing import Dict, List, Optional, Union, Any
from pathlib import Path
from pydantic import BaseModel, Field, validator, conint, constr
import os
import re

class FileInfo(BaseModel):
    """Model for file information with strict validation."""
    name: constr(min_length=1, max_length=255) = Field(
        ..., 
        description="Name of the file",
        examples=["document.txt", "image.jpg"]
    )
    path: str = Field(
        ..., 
        description="Full path to the file",
        examples=["/home/user/documents/file.txt"]
    )
    size: conint(ge=0) = Field(
        ..., 
        description="Size of the file in bytes",
        examples=[1024, 2048]
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

    @validator('path')
    def validate_path(cls, v: str) -> str:
        """Validate and sanitize file path."""
        # Normalize path separators and remove any potential directory traversal
        clean_path = os.path.normpath(v)
        if '..' in clean_path:
            raise ValueError("Path contains invalid parent directory references")
        if not os.path.isabs(clean_path):
            raise ValueError("Path must be absolute")
        return clean_path

    @validator('name')
    def validate_name(cls, v: str) -> str:
        """Validate filename."""
        if not v or v.strip() != v:
            raise ValueError("Invalid filename: must not be empty or contain leading/trailing whitespace")
        if os.path.sep in v or (os.path.altsep and os.path.altsep in v):
            raise ValueError("Filename contains path separators")
        if re.search(r'[<>:"|?*]', v):
            raise ValueError("Filename contains invalid characters")
        return v

    class Config:
        """Model configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            Path: str
        }
        schema_extra = {
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

class DirectoryStats(BaseModel):
    """Model for directory analysis results with validation."""
    total_size: conint(ge=0) = Field(
        0, 
        description="Total size of all files in bytes"
    )
    file_count: conint(ge=0) = Field(
        0, 
        description="Number of files"
    )
    dir_count: conint(ge=0) = Field(
        0, 
        description="Number of directories"
    )
    extensions: Dict[str, int] = Field(
        default_factory=dict,
        description="Count of file extensions"
    )
    by_category: Dict[str, Dict[str, int]] = Field(
        default_factory=dict,
        description="Files grouped by category"
    )

    @validator('extensions')
    def validate_extensions(cls, v: Dict[str, int]) -> Dict[str, int]:
        """Validate extension counts."""
        return {ext.lower(): count for ext, count in v.items()}

    class Config:
        """Model configuration."""
        schema_extra = {
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
    result: Optional[Union[str, Path, Dict[str, Any]]] = Field(
        None,
        description="Operation result data"
    )

    class Config:
        """Model configuration."""
        json_encoders = {Path: str}
        schema_extra = {
            "example": {
                "success": True,
                "error_message": None,
                "result": "/path/to/processed/file.txt"
            }
        }

class FileHash(BaseModel):
    """Model for file hash results with algorithm validation."""
    algorithm: constr(regex='^(md5|sha1|sha256|sha512)$') = Field(
        ..., 
        description="Hash algorithm used"
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

    @validator('algorithm')
    def validate_algorithm(cls, v: str) -> str:
        """Validate hash algorithm."""
        return v.lower()

    @validator('hash_value')
    def validate_hash(cls, v: str, values: Dict[str, Any]) -> str:
        """Validate hash value format."""
        if 'algorithm' in values:
            expected_length = {
                'md5': 32,
                'sha1': 40,
                'sha256': 64,
                'sha512': 128
            }[values['algorithm']]
            if len(v) != expected_length:
                raise ValueError(
                    f"Hash length mismatch for {values['algorithm']}: "
                    f"expected {expected_length}, got {len(v)}"
                )
        if not re.match(r'^[a-fA-F0-9]+$', v):
            raise ValueError("Hash value must contain only hexadecimal characters")
        return v.lower()

    class Config:
        """Model configuration."""
        schema_extra = {
            "example": {
                "algorithm": "sha256",
                "hash_value": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                "file_path": "/path/to/file.txt"
            }
        }

class CategoryConfig(BaseModel):
    """Model for file category configuration with validation."""
    name: constr(min_length=1, max_length=50) = Field(
        ..., 
        description="Category name"
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

    @validator('extensions', each_item=True)
    def validate_extension(cls, v: str) -> str:
        """Validate file extension."""
        if not v.startswith('.'):
            v = f'.{v}'
        if not re.match(r'^\.[a-zA-Z0-9]+$', v):
            raise ValueError("Invalid file extension format")
        return v.lower()

    class Config:
        """Model configuration."""
        schema_extra = {
            "example": {
                "name": "documents",
                "extensions": [".pdf", ".doc", ".txt"],
                "description": "Text-based document files"
            }
        } 