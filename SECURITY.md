# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 2.0.x   | Yes                |
| 1.1.x   | Security fixes only|
| < 1.1   | No                 |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly.

### How to Report

1. **Do NOT** open a public GitHub issue for security vulnerabilities.
2. Email the maintainer at [montycraig@users.noreply.github.com](mailto:montycraig@users.noreply.github.com) with:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### Response Timeline

- **Acknowledgment**: Within 48 hours
- **Initial assessment**: Within 1 week
- **Fix timeline**: Depends on severity (critical: 24-72 hours, high: 1 week, medium: 2 weeks)

### What to Expect

- Confirmation that we received your report
- An assessment of the vulnerability and its severity
- A timeline for the fix
- Credit in the release notes (unless you prefer anonymity)

## Security Considerations

### File Operations

- All file operations use safe wrappers with validation
- Path traversal attacks are prevented by path normalization and validation
- Destructive operations require explicit confirmation
- Secure deletion overwrites file contents before unlinking

### Input Validation

- All file paths are validated and normalized (no `..` traversal)
- Filenames are checked for invalid characters and path separators
- Pydantic v2 models enforce strict type validation on all data
- File extensions are normalized to prevent bypass attacks

### Configuration

- Configuration files are stored in user home directory with appropriate permissions
- No sensitive data (passwords, tokens) is stored in configuration
- Configuration parsing handles malformed JSON gracefully without crashing

### Dependencies

- Dependencies are pinned to known-good versions
- Regular dependency audits via `pip-audit` and Dependabot
- Minimal dependency footprint to reduce attack surface

## Best Practices for Users

1. Run with least-privilege permissions
2. Review `--dry-run` output before executing bulk operations
3. Keep the tool updated to the latest version
4. Report any unexpected behavior
