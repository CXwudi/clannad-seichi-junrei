#!/usr/bin/env python3
import os
import sys
import logging
import argparse
from pathlib import Path
from collections import defaultdict
from typing import Tuple, List, Dict, Any

# Global logger
logger: logging.Logger

def setup_logging(verbose: bool = False) -> None:
    """Setup logging configuration."""
    global logger
    level: int = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logger = logging.getLogger(__name__)

def count_items_in_folder(folder_path: Path) -> Tuple[int, int, int]:
    """Count the number of files and folders in a given directory."""
    try:
        items: List[Path] = list(Path(folder_path).iterdir())
        files: int = sum(1 for item in items if item.is_file())
        folders: int = sum(1 for item in items if item.is_dir())
        total: int = len(items)
        logger.debug("Analyzed %s: %d files, %d folders, %d total", folder_path, files, folders, total)
        return files, folders, total
    except OSError as e:
        logger.error("Error accessing %s: %s", folder_path, e)
        return 0, 0, 0

def analyze_folder_stats(input_folder: str) -> None:
    """Analyze statistics for each subfolder in the input folder."""
    input_path: Path = Path(input_folder)
    
    if not input_path.exists():
        logger.error("Input folder '%s' does not exist.", input_folder)
        return
    
    if not input_path.is_dir():
        logger.error("'%s' is not a directory.", input_folder)
        return
    
    logger.info("Starting analysis of folder: %s", input_folder)
    folder_stats: List[Dict[str, Any]] = []
    
    # Get all subdirectories in the input folder
    try:
        subdirs: List[Path] = [item for item in input_path.iterdir() if item.is_dir()]
        logger.info("Found %d subdirectories to analyze", len(subdirs))
    except OSError as e:
        logger.error("Error accessing input folder: %s", e)
        return
    
    if not subdirs:
        logger.warning("No subdirectories found in '%s'", input_folder)
        return
    
    # Analyze each subdirectory
    for subdir in subdirs:
        logger.debug("Processing subdirectory: %s", subdir.name)
        files, folders, total = count_items_in_folder(subdir)
        folder_stats.append({
            'name': subdir.name,
            'path': str(subdir),
            'files': files,
            'folders': folders,
            'total': total
        })
    
    # Sort by total count (most to least)
    folder_stats.sort(key=lambda x: x['total'], reverse=True)
    logger.info("Analysis complete, displaying results")
    
    # Display results
    print(f"\nFolder Statistics for: {input_folder}")
    print("=" * 80)
    print(f"{'Folder Name':<30} {'Files':<8} {'Folders':<8} {'Total':<8}")
    print("-" * 80)
    
    for stats in folder_stats:
        print(f"{stats['name']:<30} {stats['files']:<8} {stats['folders']:<8} {stats['total']:<8}")
    
    print("-" * 80)
    print(f"Total subdirectories analyzed: {len(folder_stats)}")
    
    # Summary statistics
    total_files: int = sum(stats['files'] for stats in folder_stats)
    total_folders: int = sum(stats['folders'] for stats in folder_stats)
    total_items: int = sum(stats['total'] for stats in folder_stats)
    
    print(f"Grand total - Files: {total_files}, Folders: {total_folders}, Items: {total_items}")
    
    logger.info("Analysis summary: %d folders, %d files, %d subfolders, %d total items", len(folder_stats), total_files, total_folders, total_items)

def setup_argument_parser() -> argparse.ArgumentParser:
    """Setup and return the argument parser."""
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description='Analyze folder statistics by counting files and folders in each subdirectory',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python folder_stats.py /path/to/folder
  python folder_stats.py --verbose /path/to/folder
  python folder_stats.py -v C:\\Users\\Documents
        '''
    )
    
    parser.add_argument(
        'input_folder',
        help='Path to the folder containing subdirectories to analyze'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging (debug level)'
    )
    
    return parser

def main() -> None:
    parser: argparse.ArgumentParser = setup_argument_parser()
    args: argparse.Namespace = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    
    # Run analysis
    analyze_folder_stats(args.input_folder)

if __name__ == "__main__":
    main()