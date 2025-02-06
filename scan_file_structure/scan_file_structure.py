import os
import argparse
import sys
from pathlib import Path

try:
    import pathspec
except ImportError:
    print("The 'pathspec' library is required to run this script.")
    print("Install it using: pip install pathspec")
    sys.exit(1)

def load_gitignore(root_path):
    gitignore_path = os.path.join(root_path, '.gitignore')
    if not os.path.isfile(gitignore_path):
        return None  # No .gitignore file found

    try:
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            gitignore_content = f.read()
        spec = pathspec.PathSpec.from_lines('gitwildmatch', gitignore_content.splitlines())
        return spec
    except Exception as e:
        print(f"Error reading .gitignore file: {e}")
        return None

def scan_directory(path, prefix, spec):
    try:
        # Retrieve and sort directory contents
        items = sorted(os.listdir(path))
    except PermissionError:
        print(f"{prefix}Permission denied: {path}")
        return
    except FileNotFoundError:
        print(f"{prefix}Path not found: {path}")
        return

    # Iterate through items with their indices
    for index, item in enumerate(items):
        # Skip .git folder and .gitignore file
        if item == '.git' or item == '.gitignore':
            continue

        item_path = os.path.join(path, item)
        relative_path = os.path.relpath(item_path, start=root_path)
        
        # Check if the item matches any ignore patterns
        if spec and spec.match_file(relative_path):
            continue  # Skip ignored files/directories

        connector = "├── " if index < len(items) - 1 else "└── "
        print(f"{prefix}{connector}{item}")

        # If item is a directory, recurse into it
        if os.path.isdir(item_path):
            # Determine the new prefix for the next level
            extension = "│   " if index < len(items) - 1 else "    "
            scan_directory(item_path, prefix + extension, spec)

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Recursively scan directories and output the file structure to the console, respecting .gitignore rules."
    )
    parser.add_argument("path", help="Path of the directory to scan")
    args = parser.parse_args()

    # Normalize the provided path
    global root_path
    root_path = os.path.abspath(args.path)

    # Validate the provided path
    if not os.path.exists(root_path):
        print(f"Error: The path '{root_path}' does not exist.")
        sys.exit(1)

    if not os.path.isdir(root_path):
        print(f"Error: The path '{root_path}' is not a directory.")
        sys.exit(1)

    # Load .gitignore specifications if present
    spec = load_gitignore(root_path)

    # Print the root directory
    print(root_path)
    # Start scanning from the root directory
    scan_directory(root_path, "", spec)

if __name__ == "__main__":
    main()
