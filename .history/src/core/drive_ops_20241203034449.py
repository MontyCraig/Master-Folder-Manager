"""
Drive operations module for Enhanced Folder Manager.

License: MetaReps Copyright 2024 - 2025
"""

import psutil
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging
from rich.tree import Tree
from datetime import datetime

from src.config import settings

logger = logging.getLogger(__name__)

def get_volume_info(path: Path) -> Dict[str, Any]:
    """Get detailed information about a volume."""
    try:
        usage = psutil.disk_usage(str(path))
        return {
            "total": usage.total,
            "used": usage.used,
            "free": usage.free,
            "percent": usage.percent,
            "mount_point": str(path),
            "device": None,  # Will be populated if found
            "fstype": None   # Will be populated if found
        }
    except Exception as e:
        logger.error(f"Error getting volume info for {path}: {str(e)}")
        raise

def get_all_volumes() -> List[Dict[str, Any]]:
    """Get information about all mounted volumes."""
    try:
        volumes = []
        partitions = psutil.disk_partitions(all=False)
        
        # Get configured volumes first
        configured_paths = settings.get_available_volumes()
        configured_paths_str = [str(p) for p in configured_paths]
        
        for partition in partitions:
            # Skip system volumes
            if partition.mountpoint.startswith(('/System', '/private')):
                continue
                
            try:
                info = get_volume_info(Path(partition.mountpoint))
                info["device"] = partition.device
                info["fstype"] = partition.fstype
                
                # Mark if this is a configured volume
                info["is_configured"] = partition.mountpoint in configured_paths_str
                
                volumes.append(info)
            except Exception:
                continue
                
        # Sort volumes: configured first, then by mount point
        volumes.sort(key=lambda x: (not x["is_configured"], x["mount_point"]))
        return volumes
        
    except Exception as e:
        logger.error(f"Error getting volumes: {str(e)}")
        raise

def scan_directory(
    path: Path,
    max_depth: int = 2,
    exclude_patterns: List[str] = None
) -> Dict[str, Any]:
    """
    Scan directory and return detailed information.
    
    Args:
        path: Directory to scan
        max_depth: Maximum depth to scan
        exclude_patterns: Patterns to exclude
        
    Returns:
        Dictionary containing scan results
    """
    try:
        if exclude_patterns is None:
            config = settings.load_config()
            exclude_patterns = config["excluded_patterns"]
            
        stats = {
            "total_size": 0,
            "file_count": 0,
            "dir_count": 0,
            "extensions": {},
            "categories": {},
            "recent_files": [],
            "large_files": []
        }
        
        def should_exclude(p: Path) -> bool:
            return any(pattern in str(p) for pattern in exclude_patterns)
            
        def process_file(file_path: Path, depth: int):
            if depth > max_depth or should_exclude(file_path):
                return
                
            try:
                file_stat = file_path.stat()
                file_info = {
                    "path": file_path,
                    "size": file_stat.st_size,
                    "modified": datetime.fromtimestamp(file_stat.st_mtime)
                }
                
                stats["total_size"] += file_info["size"]
                
                if file_path.is_file():
                    stats["file_count"] += 1
                    ext = file_path.suffix.lower()
                    stats["extensions"][ext] = stats["extensions"].get(ext, 0) + 1
                    
                    # Track by category
                    category = settings.get_category_for_file(file_path.name)
                    stats["categories"][category] = stats["categories"].get(category, 0) + 1
                    
                    # Track large and recent files
                    stats["large_files"].append((file_path, file_info["size"]))
                    stats["recent_files"].append((file_path, file_info["modified"]))
                    
                elif file_path.is_dir():
                    stats["dir_count"] += 1
                    
            except Exception as e:
                logger.warning(f"Error processing {file_path}: {str(e)}")
                
        def scan_recursive(current_path: Path, depth: int = 0):
            try:
                for item in current_path.iterdir():
                    process_file(item, depth)
                    if item.is_dir() and depth < max_depth:
                        scan_recursive(item, depth + 1)
            except Exception as e:
                logger.warning(f"Error scanning {current_path}: {str(e)}")
                
        # Start scan
        scan_recursive(path)
        
        # Sort and limit lists
        stats["large_files"].sort(key=lambda x: x[1], reverse=True)
        stats["large_files"] = stats["large_files"][:10]
        
        stats["recent_files"].sort(key=lambda x: x[1], reverse=True)
        stats["recent_files"] = stats["recent_files"][:10]
        
        return stats
        
    except Exception as e:
        logger.error(f"Error scanning directory {path}: {str(e)}")
        raise

def build_directory_tree(
    path: Path,
    max_depth: int = 3,
    exclude_patterns: List[str] = None,
    current_depth: int = 0
) -> Tree:
    """Build a visual directory tree."""
    try:
        if exclude_patterns is None:
            config = settings.load_config()
            exclude_patterns = config["excluded_patterns"]
            
        path = Path(path).resolve()
        tree = Tree(
            f"[bold blue]{path.name}[/bold blue] "
            f"([green]{path}[/green])"
        )
        
        if current_depth >= max_depth:
            return tree
            
        try:
            items = [
                item for item in path.iterdir()
                if not any(pattern in str(item) for pattern in exclude_patterns)
            ]
            
            # Sort: directories first, then files
            items.sort(key=lambda x: (not x.is_dir(), x.name.lower()))
            
            for item in items:
                if item.is_dir():
                    subtree = build_directory_tree(
                        item,
                        max_depth,
                        exclude_patterns,
                        current_depth + 1
                    )
                    tree.add(subtree)
                else:
                    size = item.stat().st_size
                    size_str = f"{size/1024/1024:.1f}MB" if size > 1024*1024 else f"{size/1024:.1f}KB"
                    tree.add(f"[cyan]{item.name}[/cyan] ([green]{size_str}[/green])")
                    
        except PermissionError:
            tree.add("[red]Permission denied[/red]")
            
        return tree
        
    except Exception as e:
        logger.error(f"Error building directory tree: {str(e)}")
        raise 