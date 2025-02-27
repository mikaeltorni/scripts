#!/usr/bin/env python
"""
analyze_folder_files.py

This script recursively processes all files in a given folder.
For each file, it reads the contents and sends them along with a system prompt
to the Gemini LLM (model "gemini-2.0-flash-thinking-exp-01-21") for analysis (grammar checking and XML/Markdown validation).
The responses are aggregated into a single timestamped output file with clear separators.
Note: The script excludes the .git folder, .gitignore file, and any files/patterns listed in .gitignore from processing.
"""

import os
import argparse
import datetime
from google import genai
from google.genai import types
import pathspec

def get_gitignore_patterns(folder_path):
    """
    Reads .gitignore file and returns a PathSpec object for pattern matching.
    Returns None if no .gitignore exists.
    """
    gitignore_path = os.path.join(folder_path, '.gitignore')
    if os.path.exists(gitignore_path):
        try:
            with open(gitignore_path, 'r', encoding='utf-8') as f:
                gitignore = pathspec.PathSpec.from_lines('gitwildmatch', f)
                return gitignore
        except Exception as e:
            print(f"Error reading .gitignore file: {e}")
    return None

def analyze_file(file_path, client):
    """
    Reads the file content and calls the Gemini LLM for analysis.
    Returns the LLM's response text (or None on error).
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

    # Define the system prompt to instruct the LLM.
    system_prompt = (
        "You are an expert language editor. Please analyze the following text carefully for any grammar errors. "
        "Additionally, if the text is in XML or Markdown format, check that the structure and formatting are correct. "
        "Consider if any changes are needed at all and provide detailed suggestions for improvements or confirm that no changes are needed."
    )
    
    # Create the prompt by combining file information, content, and instructions.
    prompt = f"File: {file_path}\n\nContent:\n{content}\n\n{system_prompt}"
    
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash-thinking-exp-01-21',
            contents=prompt
        )
        return response.text
    except Exception as e:
        print(f"Error processing file {file_path} with LLM: {e}")
        return None

def process_folder(folder_path, client):
    """
    Recursively walks through the folder and processes every file,
    excluding the .git folder, .gitignore file, and files matching .gitignore patterns.
    Returns a list of tuples: (file_path, analysis_result).
    """
    results = []
    gitignore = get_gitignore_patterns(folder_path)
    
    for root, dirs, files in os.walk(folder_path):
        # Exclude the .git directory from recursion
        if ".git" in dirs:
            dirs.remove(".git")
            
        # Remove directories that match gitignore patterns
        if gitignore:
            dirs[:] = [d for d in dirs if not gitignore.match_file(os.path.relpath(os.path.join(root, d), folder_path))]
            
        for file in files:
            # Skip .gitignore file
            if file == ".gitignore":
                continue
                
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, folder_path)
            
            # Skip files that match gitignore patterns
            if gitignore and gitignore.match_file(rel_path):
                continue
                
            print(f"Processing file: {file_path}")
            analysis = analyze_file(file_path, client)
            if analysis is not None:
                results.append((file_path, analysis))
    return results

def write_output(results):
    """
    Writes the analysis results for all files to a timestamped output file.
    Each file's output is separated by a line of equal signs.
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"analysis_{timestamp}.txt"
    separator = "\n" + "=" * 30 + "\n"
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            for file_path, analysis in results:
                f.write(f"File: {file_path}\n")
                f.write(analysis)
                f.write(separator)
        print(f"Analysis written to {output_filename}")
    except Exception as e:
        print(f"Error writing output file: {e}")

def main():
    parser = argparse.ArgumentParser(description="Analyze files in a folder using the Gemini LLM.")
    parser.add_argument("folder", help="Path to the folder to analyze")
    args = parser.parse_args()
    
    # Check that the API key is set as an environment variable.
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("Error: Please set the GOOGLE_API_KEY environment variable.")
        return
    
    # Configure the Google Generative AI client with your API key and v1alpha version.
    client = genai.Client(
        api_key=api_key,
        http_options={'api_version': 'v1alpha'}
    )
    
    results = process_folder(args.folder, client)
    if results:
        write_output(results)
    else:
        print("No files were processed.")

if __name__ == "__main__":
    main()
