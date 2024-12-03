"""
Configuration settings for Enhanced Folder Manager.

License: MetaReps Copyright 2024 - 2025
"""

from pathlib import Path
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

logger = logging.getLogger(__name__)
console = Console()

DEFAULT_CONFIG = {
    "master_folder_root": "/Volumes/Seagate_2/Master Folders",
    "quick_access_volumes": [
        "/Volumes/Seagate_2",
        "/Volumes/Seagate",
        "/Volumes/MongoDB",
        "/Volumes/MetaReps",
        "/Volumes/Willie",
        "/Volumes/One Touch",
        "/Volumes/4 TB Monty"
    ],
    "categories": {
        "Coding_Projects": {
            "extensions": [".py", ".js", ".java", ".cpp", ".h", ".html", ".css", ".php"],
            "priority": 1
        },
        "Documents": {
            "extensions": [".pdf", ".doc", ".docx", ".txt", ".md", ".xlsx", ".csv"],
            "priority": 2
        },
        "Images": {
            "extensions": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".raw"],
            "priority": 3
        },
        "Music": {
            "extensions": [".mp3", ".wav", ".flac", ".m4a", ".aac", ".ogg"],
            "priority": 4
        },
        "Videos": {
            "extensions": [".mp4", ".avi", ".mov", ".wmv", ".flv", ".mkv"],
            "priority": 5
        },
        "Archives": {
            "extensions": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
            "priority": 6
        },
        "Applications": {
            "extensions": [".app", ".exe", ".dmg", ".pkg"],
            "priority": 7
        },
        "Development": {
            "extensions": [".git", ".env", ".json", ".yaml", ".xml"],
            "priority": 8
        }
    },
    "recent_paths": [],
    "favorites": [],
    "excluded_patterns": [
        ".git",
        "__pycache__",
        "node_modules",
        ".DS_Store",
        ".Trash"
    ]
}

CONFIG_FILE = Path.home() / ".efm_config.json"

def get_category_for_file(filename: str) -> str:
    """Get appropriate category for a file based on extension."""
    try:
        config = load_config()
        ext = Path(filename).suffix.lower()
        
        for category, info in config["categories"].items():
            if ext in info["extensions"]:
                return category
        return "Other"
        
    except Exception as e:
        logger.error(f"Error determining category for {filename}: {str(e)}")
        return "Other"

def select_master_folder() -> Optional[Path]:
    """Interactive master folder selection or creation."""
    try:
        config = load_config()
        root = Path(config["master_folder_root"])
        
        if not root.exists():
            root.mkdir(parents=True, exist_ok=True)
            
        # Get existing master folders
        folders = [d for d in root.iterdir() if d.is_dir()]
        
        # Display master folders
        table = Table(title="Master Folders")
        table.add_column("Index", style="cyan", justify="right")
        table.add_column("Name", style="green")
        table.add_column("Path", style="blue")
        
        for idx, folder in enumerate(folders, 1):
            table.add_row(str(idx), folder.name, str(folder))
        
        console.print(table)
        
        # Show options
        console.print("\n[cyan]Options:[/cyan]")
        console.print("1-N: Select existing folder")
        console.print("n: Create new folder")
        console.print("b: Back to main menu")
        console.print("q: Quit program")
        
        choice = Prompt.ask(
            "Select option",
            choices=[str(i) for i in range(1, len(folders) + 1)] + ['n', 'b', 'q']
        ).lower()
        
        if choice == 'q':
            console.print("[cyan]Goodbye![/cyan]")
            exit(0)
        elif choice == 'b':
            return None
        elif choice == 'n':
            name = Prompt.ask("Enter new folder name")
            new_folder = root / name
            new_folder.mkdir(exist_ok=True)
            console.print(f"[green]Created new folder: {new_folder}[/green]")
            return new_folder
        elif choice.isdigit() and 1 <= int(choice) <= len(folders):
            return folders[int(choice) - 1]
            
        return None
        
    except Exception as e:
        logger.error(f"Error selecting master folder: {str(e)}")
        return None

def load_config() -> Dict[str, Any]:
    """Load configuration from file or create default."""
    try:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE) as f:
                config = json.load(f)
                logger.info("Loaded configuration from file")
                return config
        else:
            save_config(DEFAULT_CONFIG)
            logger.info("Created default configuration")
            return DEFAULT_CONFIG

    except Exception as e:
        logger.error(f"Error loading config: {str(e)}")
        return DEFAULT_CONFIG

def save_config(config: Dict[str, Any]) -> None:
    """Save configuration to file."""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
        logger.info("Saved configuration to file")

    except Exception as e:
        logger.error(f"Error saving config: {str(e)}")
        raise

def get_available_volumes() -> List[Path]:
    """Get list of available volumes."""
    try:
        config = load_config()
        volumes = []
        for path in config["quick_access_volumes"]:
            vol_path = Path(path)
            if vol_path.exists() and vol_path.is_mount():
                volumes.append(vol_path)
        return volumes

    except Exception as e:
        logger.error(f"Error getting volumes: {str(e)}")
        return []

def get_master_folder() -> Path:
    """Get master folder path."""
    config = load_config()
    return Path(config["master_folder_root"])

def update_recent_path(path: Path) -> None:
    """Update recent paths list."""
    try:
        config = load_config()
        path_str = str(path)
        
        if path_str in config["recent_paths"]:
            config["recent_paths"].remove(path_str)
        config["recent_paths"].insert(0, path_str)
        
        # Keep only last 10 paths
        config["recent_paths"] = config["recent_paths"][:10]
        save_config(config)

    except Exception as e:
        logger.error(f"Error updating recent paths: {str(e)}")
        raise 