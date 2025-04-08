"""
Drive operations module for Enhanced Folder Manager.

License: MetaReps Copyright 2024 - 2025
"""

import psutil
import os
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import logging
from rich.tree import Tree
from datetime import datetime

from src.config import settings
from src.core.file_ops import get_file_info

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
    volumes = []
    try:
        for part in psutil.disk_partitions(all=True):
            try:
                usage = psutil.disk_usage(part.mountpoint)
                # Calculate percent if not available
                percent = getattr(usage, 'percent', None)
                if percent is None and usage.total > 0:
                    percent = (usage.used / usage.total) * 100
                elif percent is None:
                    percent = 0
                
                volumes.append({
                    "device": part.device,
                    "mount_point": part.mountpoint,
                    "fstype": part.fstype,
                    "opts": part.opts,
                    "total": usage.total,
                    "used": usage.used,
                    "free": usage.free,
                    "percent": percent
                })
            except Exception as e:
                logger.error(f"Error getting volume info for {part.mountpoint}: {str(e)}")
    except Exception as e:
        logger.error(f"Error getting volumes: {str(e)}")
    return volumes

def scan_directory(
    path: Path,
    include_hidden: bool = False,
    max_depth: Optional[int] = None
) -> Dict[str, Any]:
    """
    Scan a directory and gather file information.
    
    Args:
        path: Directory path to scan
        include_hidden: Whether to include hidden files/directories
        max_depth: Maximum depth to scan
        
    Returns:
        Dictionary with files and directories info
    """
    results = {
        "files": [],
        "dirs": [],
        "total_size": 0,
        "total_files": 0,
        "total_dirs": 0
    }
    
    try:
        if not path.exists():
            raise FileNotFoundError(f"Directory not found: {path}")
            
        # Calculate max depth for recursion
        current_depth = len(path.parts)
        
        def get_relative_path(p: Path):
            return str(p.relative_to(path))
        
        def scan_item(item: Path, depth: int):
            if max_depth is not None and depth > max_depth:
                return
                
            if include_hidden is False and item.name.startswith('.'):
                return
                
            info_op = get_file_info(item)
            if not info_op.success or not info_op.result:
                logger.warning(f"Failed to get info for {item}: {info_op.error_message}")
                return
                
            info = info_op.result
            
            # Add to results
            if info.is_dir:
                results["dirs"].append(info)
                results["total_dirs"] += 1
                
                # Scan subdirectories recursively
                for child in item.iterdir():
                    scan_item(child, depth + 1)
            else:
                results["files"].append(info)
                results["total_files"] += 1
                results["total_size"] += info.size
                
        # Start recursive scan
        for item in path.iterdir():
            scan_item(item, current_depth + 1)
            
        return results
    except Exception as e:
        logger.error(f"Error scanning directory: {str(e)}")
        # Return empty results structure to avoid key errors
        return {
            "files": [],
            "dirs": [],
            "total_size": 0,
            "total_files": 0,
            "total_dirs": 0
        }

def build_directory_tree(
    path: Path,
    max_depth: Optional[int] = None,
    exclude_patterns: List[str] = None,
    include_patterns: List[str] = None
) -> Dict[str, Any]:
    """
    Build a tree representation of directory structure.
    
    Args:
        path: Root directory path
        max_depth: Maximum depth to traverse
        exclude_patterns: List of glob patterns to exclude 
        include_patterns: List of glob patterns to include
        
    Returns:
        Dictionary representing directory tree
    """
    try:
        if not path.exists():
            raise FileNotFoundError(f"Directory not found: {path}")
            
        # Initialize tree with root node
        tree = {
            "name": path.name or str(path),
            "path": str(path),
            "type": "directory",
            "children": {}
        }
        
        # Starting depth
        current_depth = len(path.parts)
        
        def matches_pattern(item_path: Path, patterns: List[str]) -> bool:
            """Check if path matches any of the glob patterns"""
            if not patterns:
                return False
            return any(item_path.match(pattern) for pattern in patterns)
            
        def should_include(item_path: Path) -> bool:
            """Determine if item should be included based on patterns"""
            # Exclude has priority over include
            if exclude_patterns and matches_pattern(item_path, exclude_patterns):
                return False
                
            # If include patterns specified, path must match one
            if include_patterns:
                return matches_pattern(item_path, include_patterns)
                
            # Default is to include
            return True
            
        def build_tree_recursive(current_path: Path, current_tree: Dict, depth: int):
            """Recursively build the tree"""
            if max_depth is not None and depth > current_depth + max_depth:
                return
                
            try:
                for item in current_path.iterdir():
                    if not should_include(item):
                        continue
                        
                    # Get file info
                    info_op = get_file_info(item)
                    if not info_op.success or not info_op.result:
                        continue
                        
                    info = info_op.result
                    
                    node_key = item.name
                    if info.is_dir:
                        # Create dictionary for directory
                        current_tree[node_key] = {
                            "name": item.name,
                            "path": str(item),
                            "type": "directory",
                            "children": {}
                        }
                        
                        # Recurse into subdirectory
                        build_tree_recursive(item, current_tree[node_key]["children"], depth + 1)
                    else:
                        # Add file as leaf node
                        current_tree[node_key] = {
                            "name": item.name,
                            "path": str(item),
                            "type": "file",
                            "size": info.size,
                            "extension": item.suffix.lower() if item.suffix else None
                        }
            except Exception as e:
                logger.warning(f"Error processing {current_path}: {str(e)}")
                
        # Build the tree starting from children of root
        build_tree_recursive(path, tree["children"], current_depth)
        
        return tree
    except Exception as e:
        logger.error(f"Error building directory tree: {str(e)}")
        # Return minimal tree
        return {
            "name": path.name or str(path),
            "path": str(path),
            "type": "directory", 
            "children": {}
        } 