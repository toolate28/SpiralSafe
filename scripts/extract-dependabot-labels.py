#!/usr/bin/env python3
"""
Extract labels from Dependabot configuration.

Parses .github/dependabot.yml and outputs all unique labels in machine-readable format.
Used by CI workflows to validate label existence.

ATOM: ATOM-TASK-20260120-003-extract-dependabot-labels
"""

import sys
import yaml
from pathlib import Path


def extract_labels(dependabot_file: str) -> set[str]:
    """Extract all unique labels from dependabot.yml configuration."""
    try:
        with open(dependabot_file, 'r') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {dependabot_file}", file=sys.stderr)
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML in {dependabot_file}: {e}", file=sys.stderr)
        sys.exit(1)
    
    labels = set()
    updates = config.get('updates', [])
    
    if not updates:
        print("Warning: No 'updates' section found in dependabot.yml", file=sys.stderr)
    
    for update in updates:
        for label in update.get('labels', []):
            labels.add(label)
    
    return labels


def main():
    """Main entry point."""
    # Default to .github/dependabot.yml relative to script location
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    dependabot_file = repo_root / '.github' / 'dependabot.yml'
    
    # Allow override via command line argument
    if len(sys.argv) > 1:
        dependabot_file = Path(sys.argv[1])
    
    labels = extract_labels(str(dependabot_file))
    
    # Output one label per line (machine-readable)
    for label in sorted(labels):
        print(label)
    
    # Exit with count as return code (0 if no labels found)
    sys.exit(0 if labels else 1)


if __name__ == '__main__':
    main()
