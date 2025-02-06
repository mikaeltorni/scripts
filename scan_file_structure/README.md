# File Structure Scanner

## Description
A Python utility that recursively scans directories and outputs the file structure to the console, respecting `.gitignore` rules. This tool provides a clear, hierarchical visualization of your directory structure while intelligently excluding files and directories that match your `.gitignore` patterns.

## Features
- Recursive directory scanning
- Respects `.gitignore` rules
- Clear hierarchical visualization using tree-like structure
- Permission error handling
- Command-line interface
- UTF-8 encoding support

## Requirements
All required dependencies are listed in `requirements.txt`. The script requires Python 3.13.1.

## Installation

1. Ensure you have Python 3.13.1 installed:
```bash
python --version
```

2. Set up your environment:

### Option A: Using Conda (Recommended)
```bash
# Create a new conda environment
conda create --name file_scanner python=3.13.1

# Activate the environment
conda activate file_scanner

# Install dependencies
pip install -r requirements.txt
```

### Option B: Using virtualenv
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
.\venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage
Run the script by providing the path to the directory you want to scan:

```bash
python scan_file_structure.py <directory_path>
```

### Example
```bash
python scan_file_structure.py .
```

This will output something like:
```
C:\your\directory\path
├── folder1
│   ├── file1.txt
│   └── file2.txt
└── folder2
    └── file3.txt
```

## Notes
- The script will automatically skip the `.git` directory and `.gitignore` file
- Files and directories matching patterns in your `.gitignore` file will be excluded
- Permission denied errors will be displayed for inaccessible directories 

