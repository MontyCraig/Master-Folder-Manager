"""
Git setup and management tools.

License: MetaReps Copyright 2024 - 2025
"""

import subprocess
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from src.utils.path_manager import sanitize_config_for_github, restore_dev_paths

def setup_git():
    """Initialize Git repository with proper configuration."""
    commands = [
        ["git", "init"],
        ["git", "add", "."],
        ["git", "config", "core.excludesfile", ".gitignore"],
    ]
    
    for cmd in commands:
        subprocess.run(cmd)

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