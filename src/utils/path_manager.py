"""
Path management utilities for Enhanced Folder Manager.

License: MetaReps Copyright 2024 - 2025
"""

import json
import os
from pathlib import Path
from typing import Dict, Any

# Development paths (local)
DEV_PATHS = {
    "master_folder_root": "/Volumes/Seagate_2/Master Folders",
    "quick_access_volumes": [
        "/Volumes/Seagate_2",
        "/Volumes/Seagate",
        "/Volumes/MongoDB",
        "/Volumes/MetaReps",
        "/Volumes/Willie",
        "/Volumes/One Touch",
        "/Volumes/4 TB Monty"
    ]
}

# Generic paths (for GitHub)
GENERIC_PATHS = {
    "master_folder_root": "~/Documents/Master Folders",
    "quick_access_volumes": [
        "/Volumes/Drive1",
        "/Volumes/Drive2"
    ]
}

def sanitize_config_for_github() -> None:
    """Replace development paths with generic ones in config files."""
    config_file = Path.home() / ".efm_config.json"
    if config_file.exists():
        with open(config_file) as f:
            config = json.load(f)
            
        # Replace paths
        config["master_folder_root"] = GENERIC_PATHS["master_folder_root"]
        config["quick_access_volumes"] = GENERIC_PATHS["quick_access_volumes"]
        
        # Save sanitized config
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=4)

def restore_dev_paths() -> None:
    """Restore development paths in config files."""
    config_file = Path.home() / ".efm_config.json"
    if config_file.exists():
        with open(config_file) as f:
            config = json.load(f)
            
        # Restore paths
        config["master_folder_root"] = DEV_PATHS["master_folder_root"]
        config["quick_access_volumes"] = DEV_PATHS["quick_access_volumes"]
        
        # Save restored config
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=4) 