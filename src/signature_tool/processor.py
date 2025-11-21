"""
File processor for adding signatures to code files.

Handles reading files, detecting existing signatures, and adding new ones.
"""

import os
from pathlib import Path
from typing import Optional, List, Set

from .generator import generate_signature, is_supported_file


# Directories to skip when scanning
SKIP_DIRS = {
    '.git', '.venv', 'venv', 'env', '__pycache__', 'node_modules',
    '.pytest_cache', '.mypy_cache', 'dist', 'build', '.egg-info',
    '.tox', 'htmlcov', '.coverage', '.idea', '.vscode'
}

# Files to skip
SKIP_FILES = {
    '.gitignore', '.dockerignore', 'LICENSE', 'CHANGELOG',
    'requirements.txt', 'package-lock.json', 'yarn.lock', 'poetry.lock'
}


class FileProcessor:
    """Processes files to add or update signatures."""

    def __init__(self, config: dict, dry_run: bool = False, force: bool = False):
        """
        Initialize file processor.

        Args:
            config: Configuration dictionary
            dry_run: If True, don't modify files (just report what would change)
            force: If True, update existing signatures
        """
        self.config = config
        self.dry_run = dry_run
        self.force = force
        self.email = config['email']

    def has_signature(self, content: str) -> bool:
        """
        Check if file already has a signature.

        Args:
            content: File content

        Returns:
            True if signature (with user's email) found in first 20 lines
        """
        lines = content.split('\n')[:20]
        return any(self.email in line for line in lines)

    def process_file(self, file_path: Path) -> bool:
        """
        Process a single file, adding signature if needed.

        Args:
            file_path: Path to file

        Returns:
            True if file was modified (or would be modified in dry-run mode)
        """
        # Check if file extension is supported
        if not is_supported_file(file_path.suffix):
            return False

        # Skip if file doesn't exist or is not a file
        if not file_path.is_file():
            return False

        # Read file content
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except (UnicodeDecodeError, PermissionError):
            # Skip binary files or files we can't read
            return False

        # Check if signature already exists
        if self.has_signature(content) and not self.force:
            return False

        # Generate signature
        try:
            signature = generate_signature(self.config, file_path.suffix)
        except ValueError:
            # Unsupported file type
            return False

        # Handle shebang lines (e.g., #!/usr/bin/env python)
        if content.startswith('#!'):
            lines = content.split('\n', 1)
            shebang = lines[0] + '\n'
            rest = lines[1] if len(lines) > 1 else ''

            if self.force and self.has_signature(rest):
                # Remove old signature if forcing update
                rest = self._remove_old_signature(rest)

            new_content = shebang + '\n' + signature + rest
        else:
            if self.force and self.has_signature(content):
                # Remove old signature if forcing update
                content = self._remove_old_signature(content)

            new_content = signature + content

        # Write back (unless dry run)
        if not self.dry_run:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
            except PermissionError:
                print(f"Warning: No permission to write {file_path}")
                return False

        return True

    def _remove_old_signature(self, content: str) -> str:
        """
        Remove old signature from content.

        Args:
            content: File content

        Returns:
            Content with signature removed
        """
        lines = content.split('\n')

        # Find the end of the signature block
        # Look for separator line or email in first 20 lines
        signature_end = 0
        for i, line in enumerate(lines[:20]):
            if self.email in line:
                # Find the end marker (separator or closing comment)
                for j in range(i, min(i + 5, len(lines))):
                    if ('=====' in lines[j] or
                        '-->' in lines[j] or
                        '*/' in lines[j]):
                        signature_end = j + 1
                        break
                break

        # Skip any empty lines after signature
        while signature_end < len(lines) and not lines[signature_end].strip():
            signature_end += 1

        return '\n'.join(lines[signature_end:])

    def process_directory(self, directory: Path, files_only: Optional[List[Path]] = None) -> dict:
        """
        Process all files in a directory.

        Args:
            directory: Directory to process
            files_only: If provided, only process these specific files

        Returns:
            Dictionary with statistics: {'processed': int, 'skipped': int, 'files': list}
        """
        stats = {
            'processed': 0,
            'skipped': 0,
            'files': []
        }

        if files_only:
            # Process only specified files
            for file_path in files_only:
                if self.process_file(file_path):
                    stats['processed'] += 1
                    stats['files'].append(str(file_path))
                else:
                    stats['skipped'] += 1
        else:
            # Recursively process directory
            for root, dirs, files in os.walk(directory):
                # Skip certain directories
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

                for filename in files:
                    # Skip certain files
                    if filename in SKIP_FILES:
                        continue

                    file_path = Path(root) / filename

                    if self.process_file(file_path):
                        stats['processed'] += 1
                        stats['files'].append(str(file_path))
                    else:
                        stats['skipped'] += 1

        return stats


def process_files(config: dict, path: Path, dry_run: bool = False,
                  force: bool = False, files_only: Optional[List[Path]] = None) -> dict:
    """
    Process files to add signatures.

    Args:
        config: Configuration dictionary
        path: Path to file or directory
        dry_run: If True, don't modify files
        force: If True, update existing signatures
        files_only: If provided, only process these specific files

    Returns:
        Statistics dictionary
    """
    processor = FileProcessor(config, dry_run, force)

    if path.is_file():
        # Process single file
        success = processor.process_file(path)
        return {
            'processed': 1 if success else 0,
            'skipped': 0 if success else 1,
            'files': [str(path)] if success else []
        }
    elif path.is_dir():
        # Process directory
        return processor.process_directory(path, files_only)
    else:
        return {'processed': 0, 'skipped': 0, 'files': [], 'error': 'Path not found'}
