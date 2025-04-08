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
def rename_file(path: Union[str, Path], new_name: str) -> Path:
    """
    Rename a file.
    
    Args:
        path: Path to the file to rename
        new_name: New name for the file
        
    Returns:
        Path: New file path
        
    Raises:
        ValueError: If path or new name is invalid
        FileNotFoundError: If file doesn't exist
        FileExistsError: If destination exists
    """
    path = validate_path(path)
    
    if not path.exists():
        raise FileNotFoundError(f"File does not exist: {path}")
        
    # Validate new name
    if not new_name or new_name.strip() != new_name:
        raise ValueError("Invalid new filename")
    if os.path.sep in new_name or (os.path.altsep and os.path.altsep in new_name):
        raise ValueError("New filename contains path separators")
        
    new_path = path.parent / new_name
    if new_path.exists():
        raise FileExistsError(f"Destination already exists: {new_path}")
        
    path.rename(new_path)
    logger.info(f"Renamed {path} to {new_path}")
    return new_path

@operation_handler
def get_file_hash(path: Union[str, Path], algorithm: str = 'sha256') -> FileHash:
    """
    Calculate file hash using specified algorithm.
    
    Args:
        path: Path to the file
        algorithm: Hash algorithm to use
        
    Returns:
        FileHash: Hash result object
        
    Raises:
        ValueError: If path or algorithm is invalid
        FileNotFoundError: If file doesn't exist
    """
    path = validate_path(path)
    
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"File does not exist or is not a file: {path}")
        
    valid_algorithms = {'md5', 'sha1', 'sha256', 'sha512'}
    if algorithm.lower() not in valid_algorithms:
        raise ValueError(f"Unsupported hash algorithm. Must be one of: {valid_algorithms}")
        
    hash_obj = hashlib.new(algorithm)
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_obj.update(chunk)
            
    return FileHash(
        algorithm=algorithm,
        hash_value=hash_obj.hexdigest(),
        file_path=str(path)
    ) 