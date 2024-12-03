"""
Directory operations module for Enhanced Folder Manager.

License: MetaReps Copyright 2024 - 2025
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
import shutil
import logging
from datetime import datetime

from src.config import settings
from src.core.file_ops import get_file_info

logger = logging.getLogger(__name__)

def ensure_master_folders() -> Dict[str, Path]:
    """Ensure master folders exist in the configured location."""
    try:
        config = settings.load_config()
        root = Path(config["master_folder_root"])
        categories = config["categories"].keys()
        
        root.mkdir(parents=True, exist_ok=True)
        
        created_folders = {}
        for category in categories:
            folder_path = root / category
            folder_path.mkdir(exist_ok=True)
            created_folders[category] = folder_path
            
        return created_folders
        
    except Exception as e:
        logger.error(f"Error creating master folders: {str(e)}")
        raise

def analyze_directory(path: Path, include_hidden: bool = False) -> Dict[str, Any]:
    """Analyze directory contents."""
    try:
        stats = {
            "total_size": 0,
            "file_count": 0,
            "dir_count": 0,
            "extensions": {},
            "by_category": {}
        }
        
        for item in path.rglob("*"):
            if not include_hidden and item.name.startswith('.'):
                continue
                
            info = get_file_info(item)
            
            if info["is_file"]:
                stats["file_count"] += 1
                stats["total_size"] += info["size"]
                ext = item.suffix.lower()
                stats["extensions"][ext] = stats["extensions"].get(ext, 0) + 1
                
                category = info["category"]
                if category not in stats["by_category"]:
                    stats["by_category"][category] = {"count": 0, "total_size": 0}
                stats["by_category"][category]["count"] += 1
                stats["by_category"][category]["total_size"] += info["size"]
                
            elif info["is_dir"]:
                stats["dir_count"] += 1
                
        return stats
        
    except Exception as e:
        logger.error(f"Error analyzing directory: {str(e)}")
        raise

def organize_files(
    source_dir: Path,
    master_dir: Optional[Path] = None,
    move_files: bool = True
) -> Dict[str, int]:
    """Organize files into categories."""
    try:
        if master_dir is None:
            master_dir = settings.get_master_folder()
            
        counts = {}
        
        for item in source_dir.rglob("*"):
            if not item.is_file():
                continue
                
            info = get_file_info(item)
            category = info["category"]
            
            dest_dir = master_dir / category
            dest_dir.mkdir(exist_ok=True)
            
            dest_path = dest_dir / item.name
            
            try:
                if move_files:
                    shutil.move(str(item), str(dest_path))
                else:
                    shutil.copy2(str(item), str(dest_path))
                    
                counts[category] = counts.get(category, 0) + 1
                
            except Exception as e:
                logger.warning(f"Error processing {item}: {str(e)}")
                
        return counts
        
    except Exception as e:
        logger.error(f"Error organizing files: {str(e)}")
        raise 