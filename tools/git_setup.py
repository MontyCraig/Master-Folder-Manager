"""
Git setup and management tools.

License: MetaReps Copyright 2024 - 2025
"""

import subprocess
from pathlib import Path
import sys
import json
sys.path.append(str(Path(__file__).parent.parent))

from src.utils.path_manager import sanitize_config_for_github, restore_dev_paths, GENERIC_PATHS

def create_initial_config():
    """Create initial config file if it doesn't exist."""
    config_file = Path.home() / ".efm_config.json"
    if not config_file.exists():
        initial_config = {
            "master_folder_root": GENERIC_PATHS["master_folder_root"],
            "quick_access_volumes": GENERIC_PATHS["quick_access_volumes"],
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
        
        with open(config_file, 'w') as f:
            json.dump(initial_config, f, indent=4)
        print(f"Created initial config file: {config_file}")

def setup_git():
    """Initialize Git repository with proper configuration."""
    # Create initial config
    create_initial_config()
    
    # Set default branch to main
    subprocess.run(["git", "config", "--global", "init.defaultBranch", "main"])
    
    commands = [
        ["git", "init"],
        ["git", "branch", "-M", "main"],  # Rename master to main
        ["git", "config", "core.excludesfile", ".gitignore"],
    ]
    
    for cmd in commands:
        subprocess.run(cmd)
        
    print("Git repository initialized with 'main' as default branch")

def prepare_for_commit():
    """Prepare repository for commit by sanitizing paths."""
    sanitize_config_for_github()
    print("Paths sanitized for GitHub")

def restore_after_commit():
    """Restore development paths after commit."""
    restore_dev_paths()
    print("Development paths restored")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python git_setup.py [setup|prepare|restore]")
        sys.exit(1)
        
    action = sys.argv[1]
    if action == "setup":
        setup_git()
    elif action == "prepare":
        prepare_for_commit()
    elif action == "restore":
        restore_after_commit() 