#!/usr/bin/env python3
"""
Dependency Verification Script for SpiralSafe
Validates Python requirements files for common issues.

ATOM-INFRA-FIX-20260112-001
"""
import re
import sys
from pathlib import Path
from typing import List, Dict, Set, Tuple

# Python standard library modules that should not be in requirements
STDLIB_MODULES = {
    'asyncio', 'os', 'sys', 'json', 're', 'pathlib', 'typing', 'datetime',
    'collections', 'itertools', 'functools', 'io', 'time', 'unittest',
    'logging', 'subprocess', 'tempfile', 'shutil', 'copy', 'pickle',
    'warnings', 'abc', 'enum', 'dataclasses', 'contextlib', 'traceback'
}

# Heavy ML/quantum packages that should be optional
HEAVY_PACKAGES = {
    'torch', 'tensorflow', 'qiskit', 'jax', 'transformers', 'diffusers',
    'manim'  # Heavy mathematical animation library
}


def parse_requirement_line(line: str) -> Tuple[str, str]:
    """Parse a requirement line to extract package name and version spec."""
    line = line.strip()
    if not line or line.startswith('#'):
        return '', ''
    
    # Handle inline comments
    if '#' in line:
        line = line.split('#')[0].strip()
    
    # Extract package name (before version specifier)
    match = re.match(r'^([a-zA-Z0-9_-]+)', line)
    if match:
        return match.group(1).lower(), line
    return '', ''


def check_requirements_file(filepath: Path) -> List[Dict[str, any]]:
    """Check a requirements file for common issues."""
    issues = []
    
    if not filepath.exists():
        return issues
    
    try:
        content = filepath.read_text()
        lines = content.split('\n')
    except Exception as e:
        issues.append({
            'type': 'error',
            'file': str(filepath),
            'message': f'Failed to read file: {e}'
        })
        return issues
    
    seen_packages = {}  # package_name -> line_number
    unpinned_packages = []
    heavy_packages_found = []
    stdlib_packages = []
    
    for i, line in enumerate(lines, 1):
        package_name, full_line = parse_requirement_line(line)
        if not package_name:
            continue
        
        # Check for duplicate entries
        if package_name in seen_packages:
            issues.append({
                'type': 'error',
                'file': str(filepath),
                'line': i,
                'message': f'Duplicate package "{package_name}" (also on line {seen_packages[package_name]})'
            })
        else:
            seen_packages[package_name] = i
        
        # Check for stdlib modules
        if package_name in STDLIB_MODULES:
            stdlib_packages.append((package_name, i))
        
        # Check for unpinned versions (using >= or no version)
        if '>=' in full_line or '>' in full_line:
            if not re.search(r'[<>=]=[0-9]', full_line):
                unpinned_packages.append((package_name, i))
        
        # Check for heavy packages that should be optional
        if package_name in HEAVY_PACKAGES and not line.strip().startswith('#'):
            heavy_packages_found.append((package_name, i))
    
    # Report stdlib modules
    for package, line_num in stdlib_packages:
        issues.append({
            'type': 'error',
            'file': str(filepath),
            'line': line_num,
            'message': f'"{package}" is a Python stdlib module and should not be in requirements'
        })
    
    # Report unpinned versions as warnings
    for package, line_num in unpinned_packages:
        issues.append({
            'type': 'warning',
            'file': str(filepath),
            'line': line_num,
            'message': f'"{package}" uses relaxed version constraint (consider pinning for reproducibility)'
        })
    
    # Report heavy packages (unless already in requirements-ml.txt)
    is_ml_file = 'ml' in str(filepath).lower()
    for package, line_num in heavy_packages_found:
        if not is_ml_file:
            issues.append({
                'type': 'warning',
                'file': str(filepath),
                'line': line_num,
                'message': f'Heavy package "{package}" should be optional or in separate requirements-ml.txt'
            })
    
    return issues


def find_requirements_files(root_dir: Path) -> List[Path]:
    """Find all requirements*.txt files in the repository."""
    requirements_files = set()
    
    # Common patterns for requirements files
    patterns = ['requirements*.txt', '*requirements.txt']
    
    for pattern in patterns:
        requirements_files.update(root_dir.rglob(pattern))
    
    # Filter out node_modules and .git directories, convert back to list
    return sorted([
        f for f in requirements_files
        if 'node_modules' not in str(f) and '.git' not in str(f)
    ])


def main():
    """Main entry point."""
    root_dir = Path(__file__).parent.parent
    print("=" * 70)
    print("SpiralSafe Dependency Verification")
    print("=" * 70)
    print()
    
    requirements_files = find_requirements_files(root_dir)
    
    if not requirements_files:
        print("✓ No requirements files found")
        return 0
    
    print(f"Found {len(requirements_files)} requirements file(s):")
    for f in requirements_files:
        print(f"  - {f.relative_to(root_dir)}")
    print()
    
    all_issues = []
    for req_file in requirements_files:
        issues = check_requirements_file(req_file)
        all_issues.extend(issues)
    
    # Group and display issues
    errors = [i for i in all_issues if i['type'] == 'error']
    warnings = [i for i in all_issues if i['type'] == 'warning']
    
    if errors:
        print(f"❌ Found {len(errors)} error(s):")
        print()
        for issue in errors:
            rel_path = Path(issue['file']).relative_to(root_dir)
            if 'line' in issue:
                print(f"  {rel_path}:{issue['line']}")
            else:
                print(f"  {rel_path}")
            print(f"    {issue['message']}")
            print()
    
    if warnings:
        print(f"⚠️  Found {len(warnings)} warning(s):")
        print()
        for issue in warnings:
            rel_path = Path(issue['file']).relative_to(root_dir)
            if 'line' in issue:
                print(f"  {rel_path}:{issue['line']}")
            else:
                print(f"  {rel_path}")
            print(f"    {issue['message']}")
            print()
    
    if not all_issues:
        print("✓ No issues found!")
        print()
        return 0
    
    print("=" * 70)
    print(f"Summary: {len(errors)} error(s), {len(warnings)} warning(s)")
    print("=" * 70)
    
    # Exit with error code if there are errors
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
