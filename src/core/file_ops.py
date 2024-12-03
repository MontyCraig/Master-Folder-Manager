"""
File operations module for Enhanced Folder Manager.

License: MetaReps Copyright 2024 - 2025
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
import shutil
import logging
from datetime import datetime

from src.config import settings

logger = logging.getLogger(__name__)

def get_file_info(path: Path) -> Dict[str, Any]:
    """Get detailed information about a file."""
    try:
        stats = path.stat()
        return {
            "name": path.name,
            "path": str(path),
            "size": stats.st_size,
            "modified": datetime.fromtimestamp(stats.st_mtime),
            "is_dir": path.is_dir(),
            "is_file": path.is_file(),
            "category": settings.get_category_for_file(path.name) if path.is_file() else None
        }
    except Exception as e:
        logger.error(f"Error getting file info: {str(e)}")
        raise 