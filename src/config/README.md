# Configuration Module Documentation

Technical specifications for configuration management.

## Configuration Schema

```json
{
    "master_folder_root": str,
    "quick_access_volumes": List[str],
    "categories": {
        "category_name": {
            "extensions": List[str],
            "priority": int
        }
    },
    "recent_paths": List[str],
    "favorites": List[str],
    "excluded_patterns": List[str]
}

```text
## Settings Management

### Load Process

1. Check for existing config

2. Load or create default

3. Validate structure

4. Apply user overrides

### Save Process

1. Validate changes

2. Backup existing

3. Atomic write

4. Verify integrity

## Category System

### Definition

- Extension-based matching

- Priority ordering

- Custom rules support

### Processing

1. Extension check

2. Name pattern match

3. Priority application

4. Default fallback
