#!/usr/bin/env python
"""Script to fix common Markdown linting issues."""

import os
import re
import glob
from pathlib import Path

def fix_markdown_file(file_path):
    """Fix common Markdown linting issues in a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add blank lines around headings (MD022)
    content = re.sub(r'([^\n])\n(#{1,6} )', r'\1\n\n\2', content)
    content = re.sub(r'(#{1,6} .*)\n([^\n])', r'\1\n\n\2', content)

    # Add blank lines around code fences (MD031)
    content = re.sub(r'([^\n])\n```', r'\1\n\n```', content)
    content = re.sub(r'```\n([^\n])', r'```\n\n\1', content)

    # Add language specifier to code fences (MD040)
    content = re.sub(r'```\s*\n', r'```text\n', content)

    # Surround lists with blank lines (MD032)
    content = re.sub(r'([^\n])\n(- )', r'\1\n\n\2', content)
    content = re.sub(r'([^\n])\n(\d+\. )', r'\1\n\n\2', content)
    content = re.sub(r'(- .*)\n([^\n-])', r'\1\n\n\2', content)
    content = re.sub(r'(\d+\. .*)\n([^\n\d])', r'\1\n\n\2', content)

    # Fix multiple consecutive blank lines (MD012)
    content = re.sub(r'\n{3,}', r'\n\n', content)

    # Add trailing newline (MD047)
    if not content.endswith('\n'):
        content += '\n'

    # Remove trailing spaces (MD009)
    content = re.sub(r' +\n', r'\n', content)

    # Convert URLs to Markdown links (MD034)
    url_pattern = r'(https?://[^\s]+)'
    content = re.sub(url_pattern, r'<\1>', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Fixed Markdown issues in {file_path}")

def main():
    """Find and fix Markdown files."""
    base_dir = Path(__file__).parent
    markdown_files = []

    # Find all .md files
    for ext in ["**/*.md"]:
        markdown_files.extend(glob.glob(str(base_dir / ext), recursive=True))

    for file_path in markdown_files:
        fix_markdown_file(file_path)

if __name__ == "__main__":
    main() 