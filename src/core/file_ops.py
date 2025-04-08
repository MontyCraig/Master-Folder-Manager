"""
File operations module for Enhanced Folder Manager.

License: MetaReps Copyright 2024 - 2025
"""

from pathlib import Path
from typing import Dict, List, Any, Optional, Union
import shutil
import logging
from datetime import datetime
import os
import hashlib
from functools import wraps

from src.config import settings
from src.core.models import FileInfo, FileOperation, FileHash

logger = logging.getLogger(__name__)

def operation_handler(func):
    """Decorator for handling file operations and providing consistent error handling."""
    @wraps(func)
    def wrapper(*args, **kwargs) -> FileOperation:
        try:
            result = func(*args, **kwargs)
            # If the result is already a FileOperation, return it directly
            if isinstance(result, FileOperation):
                return result
            return FileOperation(success=True, result=result)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}", exc_info=True)
            return FileOperation(success=False, error_message=str(e))
    return wrapper

def validate_path(path: Union[str, Path]) -> Path:
    """Validate and convert path to Path object."""
    try:
        if isinstance(path, str):
            path = Path(path)
        return path.resolve()
    except Exception as e:
        raise ValueError(f"Invalid path: {str(e)}")

@operation_handler
def get_file_info(path: Union[str, Path]) -> FileInfo:
    """
    Get detailed information about a file.
    
    Args:
        path: Path to the file
        
    Returns:
        FileInfo: Detailed file information
    
    Raises:
        ValueError: If path is invalid
        FileNotFoundError: If file doesn't exist
    """
    path = validate_path(path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
        
    stats = path.stat()
    return FileInfo(
        name=path.name,
        path=str(path),
        size=stats.st_size,
        modified=datetime.fromtimestamp(stats.st_mtime),
        is_dir=path.is_dir(),
        is_file=path.is_file(),
        category=settings.get_category_for_file(path.name) if path.is_file() else None
    )

@operation_handler
def safe_move_file(source: Union[str, Path], destination: Union[str, Path], overwrite: bool = False) -> bool:
    """
    Safely move a file to a new location.
    
    Args:
        source: Source file path
        destination: Destination file path
        overwrite: Whether to overwrite existing files
        
    Returns:
        bool: True if successful
        
    Raises:
        ValueError: If paths are invalid
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite is False
    """
    source = validate_path(source)
    destination = validate_path(destination)
    
    if not source.exists():
        raise FileNotFoundError(f"Source file does not exist: {source}")
        
    if destination.exists() and not overwrite:
        raise FileExistsError(f"Destination file already exists: {destination}")
        
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(source), str(destination))
    logger.info(f"Moved file from {source} to {destination}")
    return True

@operation_handler
def safe_copy_file(source: Union[str, Path], destination: Union[str, Path], overwrite: bool = False) -> bool:
    """
    Safely copy a file to a new location.
    
    Args:
        source: Source file path
        destination: Destination file path
        overwrite: Whether to overwrite existing files
        
    Returns:
        bool: True if successful
        
    Raises:
        ValueError: If paths are invalid
        FileNotFoundError: If source doesn't exist
        FileExistsError: If destination exists and overwrite is False
    """
    source = validate_path(source)
    destination = validate_path(destination)
    
    if not source.exists():
        raise FileNotFoundError(f"Source file does not exist: {source}")
        
    if destination.exists() and not overwrite:
        raise FileExistsError(f"Destination file already exists: {destination}")
        
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(str(source), str(destination))
    logger.info(f"Copied file from {source} to {destination}")
    return True

@operation_handler
def delete_file(path: Union[str, Path], secure: bool = False) -> bool:
    """
    Delete a file.
    
    Args:
        path: Path to the file to delete
        secure: Whether to perform secure deletion
        
    Returns:
        bool: True if successful
        
    Raises:
        ValueError: If path is invalid
        FileNotFoundError: If file doesn't exist
    """
    path = validate_path(path)
    
    if not path.exists():
        raise FileNotFoundError(f"File does not exist: {path}")
        
    if secure and path.is_file():
        try:
            # Perform secure deletion by overwriting with zeros
            with open(path, 'wb') as f:
                f.write(b'\x00' * path.stat().st_size)
            logger.info(f"Securely wiped file: {path}")
        except Exception as e:
            logger.error(f"Error performing secure deletion: {str(e)}")
            
    if path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)
        
    logger.info(f"Deleted {'directory' if path.is_dir() else 'file'}: {path}")
    return True

@operation_handler
def rename_file(path: Path, new_name: str) -> FileOperation:
    """
    Rename a file or directory.
    
    Args:
        path: Path to file/directory to rename
        new_name: New name for the file/directory
        
    Returns:
        FileOperation with success status and new path
    """
    try:
        if not path.exists():
            return FileOperation(success=False, error_message=f"Source path does not exist: {path}")
            
        if not new_name:
            return FileOperation(success=False, error_message="New name cannot be empty")
            
        # Validate filename
        if '/' in new_name or '\\' in new_name:
            return FileOperation(success=False, error_message="New filename contains path separators")
            
        # Create new path with same parent but new name
        new_path = path.parent / new_name
        
        # Check if destination already exists
        if new_path.exists():
            return FileOperation(success=False, error_message=f"Destination already exists: {new_path}")
            
        # Perform rename operation
        path.rename(new_path)
        
        # Return the Path object directly
        return new_path
    except Exception as e:
        logger.error(f"Error renaming file {path} to {new_name}: {e}")
        raise ValueError(str(e))

@operation_handler
def get_file_hash(path: Path, algorithm: str = "sha256") -> FileOperation:
    """
    Calculate hash of file contents.
    
    Args:
        path: Path to file
        algorithm: Hash algorithm to use
        
    Returns:
        FileOperation with success status and hash data
    """
    try:
        # Validate algorithm
        valid_algorithms = ["md5", "sha1", "sha256", "sha512"]
        if algorithm.lower() not in valid_algorithms:
            return FileOperation(
                success=False, 
                error_message=f"Unsupported hash algorithm: {algorithm}. Use one of {valid_algorithms}"
            )
            
        # Check if file exists and is a file
        if not path.exists():
            return FileOperation(success=False, error_message=f"File not found: {path}")
            
        if not path.is_file():
            return FileOperation(success=False, error_message=f"Path is not a file: {path}")
            
        # Calculate hash
        hasher = hashlib.new(algorithm.lower())
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
                
        hash_value = hasher.hexdigest()
        
        # Create a dictionary result
        result = {
            "algorithm": algorithm.lower(),
            "hash_value": hash_value,
            "path": str(path)
        }
        
        return result
    except Exception as e:
        logger.error(f"Error calculating hash for {path}: {e}")
        raise ValueError(str(e)) 