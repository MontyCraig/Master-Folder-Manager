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

DEFAULT_CATEGORIES = {
    "Documents": [".txt", ".pdf", ".doc", ".docx", ".rtf"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "Videos": [".mp4", ".avi", ".mov", ".wmv"],
    "Music": [".mp3", ".wav", ".flac", ".m4a"],
    "Downloads": [],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".js", ".java", ".cpp", ".h", ".css", ".html"],
    "Other": []
}

def ensure_master_folders(root_path: Optional[Path] = None) -> Dict[str, Path]:
    """
    Ensure master folders exist in the specified location.
    
    Args:
        root_path: Optional path to create master folders. If None, uses configured location.
    
    Returns:
        Dictionary mapping category names to their Path objects.
    """
    try:
        if root_path is None:
            config = settings.load_config()
            root_path = Path(config["master_folder_root"])
            categories = config["categories"].keys()
        else:
            categories = DEFAULT_CATEGORIES.keys()
        
        root_path.mkdir(parents=True, exist_ok=True)
        
        created_folders = {}
        for category in categories:
            folder_path = root_path / category
            folder_path.mkdir(exist_ok=True)
            created_folders[category] = folder_path
            
        return created_folders
        
    except Exception as e:
        logger.error(f"Error creating master folders: {str(e)}")
        raise

def analyze_directory(path: Path, include_hidden: bool = False) -> Dict[str, Any]:
    """
    Analyze directory contents.
    
    Args:
        path: Directory path to analyze
        include_hidden: Whether to include hidden files/directories
    
    Returns:
        Dictionary containing analysis results
    """
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
            
            # Handle FileOperation object properly
            if not info.success or not info.result:
                logger.warning(f"Could not get info for {item}: {info.error_message}")
                continue
                
            file_info = info.result
            
            if not file_info.is_dir:
                stats["file_count"] += 1
                stats["total_size"] += file_info.size
                ext = item.suffix.lower()
                stats["extensions"][ext] = stats["extensions"].get(ext, 0) + 1
                
                # Determine category
                category = "Other"
                for cat, exts in DEFAULT_CATEGORIES.items():
                    if ext in exts:
                        category = cat
                        break
                
                if category not in stats["by_category"]:
                    stats["by_category"][category] = {"count": 0, "total_size": 0}
                stats["by_category"][category]["count"] += 1
                stats["by_category"][category]["total_size"] += file_info.size
                
            else:
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
    """
    Organize files into categories.
    
    Args:
        source_dir: Source directory containing files to organize
        master_dir: Destination directory for organized files
        move_files: Whether to move files (True) or copy them (False)
    
    Returns:
        Dictionary counting files organized into each category
    """
    try:
        if master_dir is None:
            master_dir = settings.get_master_folder()
        
        # Ensure master folders exist
        ensure_master_folders(master_dir)
            
        counts = {}
        
        for item in source_dir.rglob("*"):
            if not item.is_file():
                continue
                
            # Determine category based on extension
            ext = item.suffix.lower()
            category = "Other"
            for cat, exts in DEFAULT_CATEGORIES.items():
                if ext in exts:
                    category = cat
                    break
            
            dest_dir = master_dir / category
            dest_dir.mkdir(exist_ok=True)
            
            dest_path = dest_dir / item.name
            
            # Handle duplicate filenames
            counter = 1
            while dest_path.exists():
                stem = item.stem
                if " (copy" in stem:
                    stem = stem[:stem.rindex(" (copy")]
                dest_path = dest_dir / f"{stem} (copy {counter}){item.suffix}"
                counter += 1
            
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