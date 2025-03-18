"""
Code Block Extractor

This script extracts code blocks from JSON files and saves them as separate files.
It searches for text fields in JSON data and extracts code blocks of the specified
programming language using regular expressions.

Classes:
    - CodeBlockExtractor:
        Class for extracting code blocks from JSON files and saving them to separate files.
        
        Methods:
            - __init__(self, categories: List[str] = None, tests_per_category: int = None):
                Initialize the CodeBlockExtractor with categories and tests per category.
            - get_code_block_regex(self, language: str = "python") -> re.Pattern:
                Returns a compiled regex pattern for extracting code blocks of the specified language.
            - find_text_fields(self, data: Union[Dict, List]) -> Generator[str, None, None]:
                Recursively search a data structure for any values whose key is 'text'.
            - extract_code_blocks(self, text: str, language: str = "python") -> List[str]:
                Given a text string, extract all code blocks of the specified language.
            - save_code_blocks(self, code_blocks: List[str], output_dir: str, file_extension: str = ".py") -> None:
                Save each code block to a new file with appropriate naming.
            - process_json_file(self, json_path: str, output_dir: str, language: str = "python", file_extension: str = ".py") -> int:
                Load a JSON file, search for text fields, extract code blocks, and save them to separate files.

Functions:
    - get_file_extension_for_language(language: str) -> str:
        Returns the file extension for a given programming language.
    - parse_arguments() -> argparse.Namespace:
        Parses command-line arguments for the script.
    - main() -> None:
        Main function to run the code block extraction process.
    - run_interactive_mode() -> None:
        Run the script in interactive mode, allowing the user to process multiple JSON files.

Command Line Usage:
    python main.py <json_file> [options]

Examples:
    # Extract Python code blocks from input.json and save to the default directory
    python main.py input.json

    # Extract code blocks for a different language (e.g., XML) and save to a custom directory
    python main.py input.json --output-dir my_tests --language xml --file-extension .xml

    # Extract code blocks with custom categories and verbose logging
    python main.py input.json --categories calculator contact_book --verbose
"""

import re
import json
import sys
import logging
import argparse
from pathlib import Path
from typing import List, Dict, Generator, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Default categories
DEFAULT_CATEGORIES = [
    "calculator",
    "contact_book",
    "csv_file_analysis",
    "monitor",
    "frequency_of_word",
    "quiz_game",
    "password_generator",
    "temperature_converter",
    "room_game",
    "weather_app"
]

# Default number of tests per category
DEFAULT_TESTS_PER_CATEGORY = 10

class CodeBlockExtractor:
    """
    A class for extracting code blocks from JSON files and saving them to separate files.

    This class provides methods to parse JSON files, extract code blocks from text fields,
    and save the code blocks as separate files with appropriate names.
    """

    def __init__(self, categories: List[str] = None, tests_per_category: int = None):
        """
        Initialize the CodeBlockExtractor with categories and tests per category.

        Parameters:
            categories (List[str]): List of category names for organizing code blocks
            tests_per_category (int): Number of tests per category

        Returns:
            None
        """
        print(f"[__init__] categories: {categories} | tests_per_category: {tests_per_category}")
        
        self.categories = categories or DEFAULT_CATEGORIES
        self.tests_per_category = tests_per_category or DEFAULT_TESTS_PER_CATEGORY
        
        if not isinstance(self.categories, list) or not all(isinstance(cat, str) for cat in self.categories):
            raise TypeError("[__init__] Categories must be a list of strings")
        
        if not isinstance(self.tests_per_category, int) or self.tests_per_category <= 0:
            raise ValueError("[__init__] Tests per category must be a positive integer")
        
        logger.info(f"Initialized CodeBlockExtractor with {len(self.categories)} categories and {self.tests_per_category} tests per category")

    def get_code_block_regex(self, language: str = "python") -> re.Pattern:
        """
        Returns a compiled regex pattern for extracting code blocks of the specified language.

        Parameters:
            language (str): The programming language to extract code blocks for

        Returns:
            re.Pattern: Compiled regular expression pattern
        """
        print(f"[get_code_block_regex] language: {language}")
        
        if not isinstance(language, str) or not language:
            raise ValueError("[get_code_block_regex] Language must be a non-empty string")
        
        pattern = re.compile(fr"```{language}\s*(.*?)\s*```", re.DOTALL)
        
        print(f"[get_code_block_regex] output: {pattern}")
        return pattern

    def find_text_fields(self, data: Union[Dict, List]) -> Generator[str, None, None]:
        """
        Recursively search a data structure (dict or list) for any values whose key is 'text'.
        Yields each found text value.

        Parameters:
            data (Union[Dict, List]): The data structure to search

        Returns:
            Generator[str, None, None]: Generator yielding text values
        """
        print(f"[find_text_fields] data type: {type(data)}")
        
        if not isinstance(data, (dict, list)):
            logger.warning(f"[find_text_fields] Expected dict or list, got {type(data)}")
            return
            
        if isinstance(data, dict):
            for key, value in data.items():
                if key == "text" and isinstance(value, str):
                    logger.debug(f"[find_text_fields] Found text field with {len(value)} characters")
                    yield value
                else:
                    yield from self.find_text_fields(value)
        elif isinstance(data, list):
            for item in data:
                yield from self.find_text_fields(item)
                
        print(f"[find_text_fields] finished searching {type(data)}")

    def extract_code_blocks(self, text: str, language: str = "python") -> List[str]:
        """
        Given a text string, extract all code blocks of the specified language.

        Parameters:
            text (str): The text to extract code blocks from
            language (str): The programming language to extract code blocks for

        Returns:
            List[str]: List of extracted code blocks
        """
        print(f"[extract_code_blocks] text length: {len(text)} | language: {language}")
        
        if not isinstance(text, str):
            raise TypeError("[extract_code_blocks] Text must be a string")
            
        code_block_regex = self.get_code_block_regex(language)
        code_blocks = code_block_regex.findall(text)
        
        print(f"[extract_code_blocks] output: found {len(code_blocks)} code blocks")
        return code_blocks

    def save_code_blocks(self, code_blocks: List[str], output_dir: str, file_extension: str = ".py") -> None:
        """
        Save each code block to a new file with appropriate naming.
        
        File names are generated by cycling through categories with a fixed number of files per category.
        If more code blocks are found than expected, extra ones are named with a 'test' prefix.

        Parameters:
            code_blocks (List[str]): List of code blocks to save
            output_dir (str): Directory to save the files to
            file_extension (str): File extension to use for the saved files

        Returns:
            None
        """
        print(f"[save_code_blocks] code_blocks count: {len(code_blocks)} | output_dir: {output_dir} | file_extension: {file_extension}")
        
        if not code_blocks:
            logger.warning("[save_code_blocks] No code blocks to save")
            return
            
        if not isinstance(output_dir, str):
            raise TypeError("[save_code_blocks] Output directory must be a string")
            
        if not isinstance(file_extension, str):
            raise TypeError("[save_code_blocks] File extension must be a string")
            
        if not file_extension.startswith('.'):
            file_extension = f".{file_extension}"
            logger.info(f"[save_code_blocks] Added missing dot to file extension: {file_extension}")

        # Create output directory if it doesn't exist
        output_path = Path(output_dir)
        try:
            output_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"[save_code_blocks] Created or verified output directory: {output_dir}")
        except Exception as e:
            logger.error(f"[save_code_blocks] Failed to create output directory: {e}")
            raise RuntimeError(f"[save_code_blocks] Failed to create output directory: {e}")

        # Save code blocks
        saved_count = 0
        for i, code in enumerate(code_blocks):
            try:
                # Determine which category to use based on the index
                cat_index = i // self.tests_per_category
                test_number = (i % self.tests_per_category) + 1

                if cat_index < len(self.categories):
                    category = self.categories[cat_index]
                    filename = f"{category}_{test_number}{file_extension}"
                else:
                    # If there are more code blocks than categories * TESTS_PER_CATEGORY, use a fallback name
                    filename = f"test_{i+1}{file_extension}"

                filepath = output_path / filename
                
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(code)
                
                logger.info(f"[save_code_blocks] Saved code block #{i+1} to {filepath}")
                saved_count += 1
                
            except Exception as e:
                logger.error(f"[save_code_blocks] Error saving code block #{i+1}: {e}")
                
        print(f"[save_code_blocks] output: saved {saved_count} code blocks to {output_dir}")

    def process_json_file(self, json_path: str, output_dir: str, language: str = "python", file_extension: str = ".py") -> int:
        """
        Load a JSON file, search for text fields, extract code blocks, and save them to separate files.

        Parameters:
            json_path (str): Path to the JSON file to process
            output_dir (str): Directory to save the extracted code blocks to
            language (str): Programming language to extract code blocks for
            file_extension (str): File extension to use for saved files

        Returns:
            int: Number of code blocks extracted and saved
        """
        print(f"[process_json_file] json_path: {json_path} | output_dir: {output_dir} | language: {language} | file_extension: {file_extension}")
        
        # Validate input parameters
        if not json_path or not isinstance(json_path, str):
            raise ValueError("[process_json_file] JSON path must be a non-empty string")
            
        if not output_dir or not isinstance(output_dir, str):
            raise ValueError("[process_json_file] Output directory must be a non-empty string")
            
        # Check if the JSON file exists
        json_file_path = Path(json_path)
        if not json_file_path.exists():
            error_msg = f"[process_json_file] JSON file not found: {json_path}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)
            
        # Load and parse the JSON file
        try:
            with open(json_file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            logger.info(f"[process_json_file] Successfully loaded JSON file: {json_path}")
        except json.JSONDecodeError as e:
            error_msg = f"[process_json_file] Error decoding JSON: {e}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        except Exception as e:
            error_msg = f"[process_json_file] Error reading file: {e}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

        # Gather all code blocks from every "text" field found
        all_code_blocks = []
        try:
            for text in self.find_text_fields(data):
                code_blocks = self.extract_code_blocks(text, language)
                if code_blocks:
                    logger.info(f"[process_json_file] Found {len(code_blocks)} code block(s) in a text field")
                all_code_blocks.extend(code_blocks)
        except Exception as e:
            logger.error(f"[process_json_file] Error extracting code blocks: {e}")
            raise RuntimeError(f"[process_json_file] Error extracting code blocks: {e}")

        # Save the code blocks if any were found
        if not all_code_blocks:
            logger.warning(f"[process_json_file] No code blocks found in {json_path}")
        else:
            logger.info(f"[process_json_file] Total code blocks found: {len(all_code_blocks)}")
            try:
                self.save_code_blocks(all_code_blocks, output_dir, file_extension)
            except Exception as e:
                logger.error(f"[process_json_file] Error saving code blocks: {e}")
                raise RuntimeError(f"[process_json_file] Error saving code blocks: {e}")
        
        print(f"[process_json_file] output: extracted {len(all_code_blocks)} code blocks")
        return len(all_code_blocks)


def get_file_extension_for_language(language: str) -> str:
    """
    Get the appropriate file extension for a programming language.

    Parameters:
        language (str): Programming language name

    Returns:
        str: File extension for the language
    """
    print(f"[get_file_extension_for_language] language: {language}")
    
    if not isinstance(language, str) or not language:
        raise ValueError("[get_file_extension_for_language] Language must be a non-empty string")
    
    # Mapping of language to file extension
    extension_map = {
        "python": ".py",
        "javascript": ".js",
        "typescript": ".ts",
        "java": ".java",
        "c": ".c",
        "cpp": ".cpp",
        "csharp": ".cs",
        "go": ".go",
        "ruby": ".rb",
        "php": ".php",
        "swift": ".swift",
        "kotlin": ".kt",
        "rust": ".rs",
        "scala": ".scala",
        "html": ".html",
        "css": ".css",
        "shell": ".sh",
        "bash": ".sh",
        "sql": ".sql",
        "r": ".r"
    }
    
    extension = extension_map.get(language.lower(), f".{language.lower()}")
    
    print(f"[get_file_extension_for_language] output: {extension}")
    return extension


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments for the script.

    Parameters:
        None

    Returns:
        argparse.Namespace: Parsed command-line arguments
    """
    print(f"[parse_arguments] Parsing command line arguments")
    
    parser = argparse.ArgumentParser(
        description="Parse JSON file(s) for 'text' fields and extract code blocks into separate files."
    )
    parser.add_argument(
        "json_file",
        help="Path to the JSON file to process."
    )
    parser.add_argument(
        "-o", "--output-dir",
        default="extracted_tests",
        help="Directory to save the extracted files (default: extracted_tests)"
    )
    parser.add_argument(
        "-l", "--language",
        default="python",
        help="Programming language to extract code blocks for (default: python)"
    )
    parser.add_argument(
        "-f", "--file-extension",
        help="File extension for saved files (default: determined by language)"
    )
    parser.add_argument(
        "-c", "--categories",
        nargs="+",
        help="Categories to use for naming files (space-separated list)"
    )
    parser.add_argument(
        "-t", "--tests-per-category",
        type=int,
        default=DEFAULT_TESTS_PER_CATEGORY,
        help="Number of tests per category (default: 10)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
        
    print(f"[parse_arguments] output: {args}")
    return args


def main() -> None:
    """
    Main function to run the code block extraction process.

    Parameters:
        None

    Returns:
        None
    """
    print(f"[main] Starting code block extraction")
    
    try:
        # Parse command-line arguments
        args = parse_arguments()
        
        # Set up logging level based on verbose flag
        if args.verbose:
            logger.setLevel(logging.DEBUG)
            
        # Determine file extension based on language if not provided
        file_extension = args.file_extension
        if not file_extension:
            file_extension = get_file_extension_for_language(args.language)
            
        # Create extractor with optional custom categories
        extractor = CodeBlockExtractor(
            categories=args.categories,
            tests_per_category=args.tests_per_category
        )
        
        # Process the JSON file and extract code blocks
        blocks_count = extractor.process_json_file(
            args.json_file,
            args.output_dir,
            args.language,
            file_extension
        )
        
        if blocks_count > 0:
            logger.info(f"Successfully extracted {blocks_count} code blocks to {args.output_dir}")
        else:
            logger.warning("No code blocks were extracted")
            
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        sys.exit(1)
    except ValueError as e:
        logger.error(f"Value error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)
        
    print(f"[main] Code block extraction completed")


def run_interactive_mode() -> None:
    """
    Run the script in interactive mode, allowing the user to process multiple JSON files.

    Parameters:
        None

    Returns:
        None
    """
    print(f"[run_interactive_mode] Starting interactive mode")
    
    print("\n===== Code Block Extractor - Interactive Mode =====")
    print("This program extracts code blocks from JSON files and saves them to separate files.")
    
    # Create an extractor with default settings
    extractor = CodeBlockExtractor()
    
    while True:
        try:
            # Get JSON file path
            json_path = input("\nEnter the path to the JSON file (or 'q' to quit): ").strip()
            if json_path.lower() in ('q', 'quit', 'exit'):
                print("Exiting program. Goodbye!")
                break
                
            if not json_path:
                print("Error: Please enter a valid file path.")
                continue
                
            # Check if file exists
            if not Path(json_path).exists():
                print(f"Error: File not found: {json_path}")
                continue
                
            # Get output directory
            output_dir = input("Enter output directory (or press Enter for 'extracted_tests'): ").strip()
            if not output_dir:
                output_dir = "extracted_tests"
                
            # Get language
            language = input("Enter programming language (or press Enter for 'python'): ").strip()
            if not language:
                language = "python"
                
            # Determine file extension
            file_extension = get_file_extension_for_language(language)
            
            # Process the file
            blocks_count = extractor.process_json_file(json_path, output_dir, language, file_extension)
            
            if blocks_count > 0:
                print(f"\nSuccess! Extracted {blocks_count} code blocks to {output_dir}")
            else:
                print(f"\nNo code blocks were found in {json_path}")
                
        except Exception as e:
            print(f"Error: {e}")
            
    print(f"[run_interactive_mode] Interactive mode completed")


if __name__ == "__main__":
    try:
        # Check if any command-line arguments are provided
        if len(sys.argv) > 1:
            main()
        else:
            # If no arguments provided, run in interactive mode
            run_interactive_mode()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
        sys.exit(0)
