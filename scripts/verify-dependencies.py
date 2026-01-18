#!/usr/bin/env python3
"""
Dependency Verification Script
Validates Python requirements files for common issues.

H&&S:WAVE | Hope&&Sauced
ATOM-INFRA-FIX-20260112-001
"""

import re
import sys
from pathlib import Path
from typing import List, Dict, Set, Tuple

# Stdlib modules that should never be in requirements
STDLIB_MODULES = {
    "asyncio", "typing", "json", "os", "sys", "pathlib", "datetime",
    "collections", "itertools", "functools", "re", "subprocess", "threading",
    "multiprocessing", "queue", "socket", "urllib", "http", "email", "xml",
    "sqlite3", "csv", "tempfile", "shutil", "glob", "pickle", "hashlib",
    "base64", "uuid", "random", "time", "math", "statistics", "decimal",
    "fractions", "struct", "codecs", "io", "argparse", "logging", "unittest",
    "enum", "dataclasses", "abc", "contextlib", "weakref", "copy", "pprint",
}

# Heavy packages that should be optional
HEAVY_PACKAGES = {
    "torch", "torchvision", "torchaudio", "tensorflow", "keras",
    "qiskit", "qiskit-aer", "qiskit-ibm-runtime",
    "transformers", "diffusers", "accelerate",
}


class DependencyIssue:
    """Represents a dependency validation issue."""
    
    def __init__(self, file: Path, line_num: int, severity: str, message: str):
        self.file = file
        self.line_num = line_num
        self.severity = severity
        self.message = message
    
    def __str__(self):
        return f"{self.severity.upper()}: {self.file}:{self.line_num} - {self.message}"


def parse_requirement_line(line: str) -> Tuple[str, str]:
    """Parse a requirement line to extract package name and version spec."""
    line = line.strip()
    
    # Skip comments and empty lines
    if not line or line.startswith('#'):
        return None, None
    
    # Skip -r includes
    if line.startswith('-r '):
        return None, None
    
    # Extract package name (handle ==, >=, <=, ~=, !=, <, >)
    match = re.match(r'^([a-zA-Z0-9][a-zA-Z0-9._-]*)', line)
    if match:
        package = match.group(1).lower()
        version_spec = line[len(match.group(1)):].strip()
        return package, version_spec
    
    return None, None


def check_file(file_path: Path) -> List[DependencyIssue]:
    """Check a single requirements file for issues."""
    issues = []
    
    if not file_path.exists():
        return issues
    
    try:
        content = file_path.read_text(encoding='utf-8')
        lines = content.splitlines()
    except Exception as e:
        issues.append(DependencyIssue(
            file_path, 0, "error", f"Failed to read file: {e}"
        ))
        return issues
    
    seen_packages = {}
    
    for line_num, line in enumerate(lines, 1):
        package, version_spec = parse_requirement_line(line)
        
        if package is None:
            continue
        
        # Check for stdlib modules
        if package in STDLIB_MODULES:
            issues.append(DependencyIssue(
                file_path, line_num, "error",
                f"'{package}' is a Python stdlib module and should not be in requirements"
            ))
        
        # Check for duplicates
        if package in seen_packages:
            issues.append(DependencyIssue(
                file_path, line_num, "error",
                f"Duplicate entry for '{package}' (first seen at line {seen_packages[package]})"
            ))
        else:
            seen_packages[package] = line_num
        
        # Check for unpinned versions
        if not version_spec or version_spec.startswith('>='):
            issues.append(DependencyIssue(
                file_path, line_num, "warning",
                f"'{package}' should use pinned version (==) for reproducibility"
            ))
        
        # Check for heavy packages in main requirements
        if package in HEAVY_PACKAGES and file_path.name != 'requirements-ml.txt':
            issues.append(DependencyIssue(
                file_path, line_num, "warning",
                f"Heavy package '{package}' should be in requirements-ml.txt or commented as optional"
            ))
    
    return issues


def find_requirement_files(root: Path) -> List[Path]:
    """Find all requirements*.txt files in the repository."""
    files = []
    
    # Root level requirements
    for pattern in ['requirements*.txt', '*requirements.txt']:
        files.extend(root.glob(pattern))
    
    # Subdirectory requirements
    for pattern in ['**/requirements*.txt', '**/*requirements.txt']:
        files.extend(root.glob(pattern))
    
    # Filter out node_modules, .git, etc.
    filtered = []
    for f in files:
        parts = f.parts
        if not any(skip in parts for skip in ['node_modules', '.git', 'dist', 'build', '__pycache__']):
            filtered.append(f)
    
    return sorted(set(filtered))


def main():
    """Main entry point."""
    repo_root = Path(__file__).parent.parent
    
    print("═" * 70)
    print("  SpiralSafe Dependency Verification")
    print("  H&&S:WAVE | Hope&&Sauced")
    print("═" * 70)
    print()
    
    # Find all requirements files
    req_files = find_requirement_files(repo_root)
    print(f"Found {len(req_files)} requirements file(s):\n")
    for f in req_files:
        print(f"  • {f.relative_to(repo_root)}")
    print()
    
    # Check each file
    all_issues = []
    for req_file in req_files:
        issues = check_file(req_file)
        all_issues.extend(issues)
    
    # Report results
    if not all_issues:
        print("✓ All requirements files passed validation!")
        print()
        return 0
    
    # Group by severity
    errors = [i for i in all_issues if i.severity == "error"]
    warnings = [i for i in all_issues if i.severity == "warning"]
    
    if errors:
        print(f"⚠ Found {len(errors)} ERROR(S):\n")
        for issue in errors:
            rel_path = issue.file.relative_to(repo_root)
            print(f"  {rel_path}:{issue.line_num}")
            print(f"    {issue.message}")
            print()
    
    if warnings:
        print(f"ℹ Found {len(warnings)} WARNING(S):\n")
        for issue in warnings:
            rel_path = issue.file.relative_to(repo_root)
            print(f"  {rel_path}:{issue.line_num}")
            print(f"    {issue.message}")
            print()
    
    print("─" * 70)
    print(f"Total: {len(errors)} error(s), {len(warnings)} warning(s)")
    print()
    
    # Exit with error code if there are errors
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
