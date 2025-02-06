# Log Filter
Useful for parsing logs for analyzing them with LLMs.

## Description
A Python utility that filters log files based on a search string. This tool allows you to extract specific lines containing a search term from a log file and save them to a new output file.

## Features
- Filter log files using search strings

- UTF-8 encoding support
- Command-line interface
- Error handling for file operations
- Configurable input and output files

## Requirements
The script requires Python 3.x with no additional dependencies.

## Installation
No special installation required besides Python 3.x.

## Usage
Run the script using the following command-line format:
```
python log_filter.py --search_str "your_search_string" --input "input_log_file.txt" --output "filtered_log_file.txt"
```