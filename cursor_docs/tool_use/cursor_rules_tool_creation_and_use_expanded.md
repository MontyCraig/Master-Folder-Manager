# Guidelines for AI Tools Development and Usage

## Overview

This document outlines how to create and manage tools that help AI assistants (like Claude) work more effectively with codebases. Each project should include a `tools_for_claude` directory to house these utilities.

## Project Structure

```
project_root/
├── src/
├── tools/                 # Project-specific tools
└── tools_for_claude/     # AI assistant tools
    ├── __init__.py
    ├── file_ops.py       # File operations helpers
    ├── code_analyzer.py  # Code analysis utilities
    └── doc_generator.py  # Documentation helpers
```

## Tool Categories

### 1. Code Analysis Tools

* Function/class dependency trackers
* Import analyzer
* Code complexity calculator
* Type hint validator
* Docstring completeness checker

### 2. File Operations

* File tree generator
* Project structure analyzer
* File content searcher
* Import path resolver

### 3. Documentation Helpers

* README generator
* Function documentation extractor
* API documentation compiler
* Change log generator

### 4. Code Generation

* Boilerplate generators
* Test case scaffolding
* Type hint inserter
* Error handling wrapper

## Tool Development Guidelines

### Function Design

```python
from typing import Any, Dict, List
import logging

logger = logging.getLogger(__name__)

def analyze_function(
    func_content: str,
    *,
    include_docs: bool = True,
    analyze_types: bool = True
) -> Dict[str, Any]:
    """
    Analyzes a function's content for documentation and typing.

    Args:
        func_content: The function's source code
        include_docs: Whether to analyze docstrings
        analyze_types: Whether to check type hints

    Returns:
        Dict containing analysis results
    """
    try:
        # Implementation
        pass
    except Exception as e:
        logger.error(f"Error analyzing function: {e}")
        raise
```

### Best Practices


1. **Input Validation**
   * Validate all inputs thoroughly
   * Use type hints consistently
   * Handle edge cases gracefully
2. **Error Handling**
   * Use specific exception types
   * Log errors with context
   * Provide helpful error messages
3. **Documentation**
   * Clear docstrings with examples
   * Type hints for all parameters
   * Usage instructions in comments
4. **Output Format**
   * Consistent return structures
   * Clear success/failure indicators
   * Structured data for parsing

## Common Tool Patterns

### File Scanner

```python
from pathlib import Path
from typing import Iterator

def scan_project_files(
    root: Path,
    pattern: str = "*.py"
) -> Iterator[Path]:
    """Scans project for files matching pattern."""
    return root.rglob(pattern)
```

### Code Parser

```python
import ast
from typing import List

def extract_functions(
    file_path: Path
) -> List[ast.FunctionDef]:
    """Extracts all function definitions from a file."""
    with open(file_path) as f:
        tree = ast.parse(f.read())
    return [node for node in ast.walk(tree) 
            if isinstance(node, ast.FunctionDef)]
```

## Usage Examples

### Analyzing Project Structure

```bash
python -c "from tools_for_claude.file_ops import analyze_structure; analyze_structure('.')"
```

### Generating Documentation

```bash
python -c "from tools_for_claude.doc_generator import generate_readme; generate_readme()"
```

## Tool Creation Workflow


1. **Identify Need**
   * Recognize repetitive tasks
   * Identify error-prone operations
   * Look for optimization opportunities
2. **Design**
   * Plan input/output structure
   * Consider edge cases
   * Design for reusability
3. **Implement**
   * Write clean, documented code
   * Add comprehensive error handling
   * Include usage examples
4. **Test**
   * Verify with various inputs
   * Test edge cases
   * Confirm error handling

## Maintenance

* Regular updates for new requirements
* Deprecation of unused tools
* Documentation updates
* Version control integration

## Security Considerations

* Avoid executing arbitrary code
* Sanitize file paths
* Validate all inputs
* Handle sensitive data carefully

## Notes for AI Assistants

* Create tools that complement your capabilities
* Focus on accuracy and reliability
* Maintain consistent output formats
* Log operations for debugging
* Design for human readability

## Conclusion

These tools should enhance the AI assistant's ability to:

* Analyze code effectively
* Generate accurate documentation
* Maintain consistent standards
* Reduce errors in repetitive tasks


