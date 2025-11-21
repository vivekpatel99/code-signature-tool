#!/usr/bin/env python3

# ================================================================================
# Author: Vivek Patel
# Title: AI Engineer | Computer Vision Specialist
# Website: https://vivekapatel.com
# Email: contact@vivekapatel.com
# Upwork: https://www.upwork.com/freelancers/vivekpatel99?mp_source=share
# Created: 2025-11-21
# ================================================================================
"""
Command-line interface for signature tool.

Usage:
    add-signatures [--dry-run] [--force] [--path PATH]
"""

import sys
import argparse
from pathlib import Path

from .config import load_config, ConfigError
from .processor import process_files


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description='Add professional signatures to code files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  add-signatures                    # Process current directory
  add-signatures --dry-run          # Show what would change
  add-signatures --force            # Update existing signatures
  add-signatures --path ./src       # Process specific directory
        '''
    )

    parser.add_argument(
        '--path',
        type=Path,
        default=Path.cwd(),
        help='Path to file or directory to process (default: current directory)'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be changed without modifying files'
    )

    parser.add_argument(
        '--force',
        action='store_true',
        help='Update existing signatures (preserves creation date)'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed output'
    )

    args = parser.parse_args()

    # Load configuration
    try:
        config = load_config()
    except ConfigError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        print("\nTo create a configuration file, run:", file=sys.stderr)
        print("  ./install.sh", file=sys.stderr)
        print("\nOr manually create ~/.signature.json with:", file=sys.stderr)
        print('  {"author": "Your Name", "email": "your@email.com"}', file=sys.stderr)
        sys.exit(1)

    # Validate path
    if not args.path.exists():
        print(f"Error: Path not found: {args.path}", file=sys.stderr)
        sys.exit(1)

    # Process files
    print(f"{'[DRY RUN] ' if args.dry_run else ''}Processing {args.path}...")

    try:
        stats = process_files(
            config.to_dict(),
            args.path,
            dry_run=args.dry_run,
            force=args.force
        )
    except Exception as e:
        print(f"Error processing files: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

    # Report results
    print(f"\nResults:")
    print(f"  Processed: {stats['processed']} files")
    print(f"  Skipped:   {stats['skipped']} files")

    if args.verbose and stats['files']:
        print(f"\nModified files:")
        for file_path in stats['files']:
            print(f"  - {file_path}")

    if args.dry_run and stats['processed'] > 0:
        print(f"\nRun without --dry-run to apply changes")

    sys.exit(0)


if __name__ == '__main__':
    main()
