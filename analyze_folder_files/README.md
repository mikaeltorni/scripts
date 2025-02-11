# LLM File Analyzer

This project analyzes the contents of files in a specified folder using Google's Gemini LLM (model: gemini-exp-1206). It recursively scans the folder, sends each file's content along with a system prompt to the LLM, and produces a consolidated report outlining any grammar issues or formatting suggestions (especially for XML and Markdown files). However the system prompt can be changed to anything to do with the analysis of the files.

## Features

- **Recursive Processing:** Walks through a given folder (and subfolders) to process all files.
- **LLM Analysis:** For each file, sends its content to the Gemini LLM with a system prompt that instructs the model to:
  - Check for grammar errors.
  - Verify that XML and Markdown formatting is correct.
  - Analyze the text carefully and decide if any changes are needed.
- **Deterministic Output:** Uses a temperature of 0 for consistent results.
- **Aggregated Report:** Outputs a timestamped text file where each file's analysis is separated by a line of equal signs.

## Setup

### Prerequisites

- **Python:** Latest version is recommended (e.g., Python 3.11).
- **Conda:** To create and manage an isolated environment.
- **Gemini API Key:** A valid API key for Google's Gemini LLM. (Set as an environment variable `GOOGLE_API_KEY`.)

### Create a Conda Environment

1. Open a terminal.
2. Create a new Conda environment with the latest Python version:
```bash
conda create -n llma python=3.13.2  
conda activate llma
```

3. Install the required Python packages:
```bash
pip install -r requirements.txt
```

### Set Up the API Key

Export your Gemini API key as an environment variable:
```bash
export GOOGLE_API_KEY="your_api_key_here"
```

*Tip:* To avoid setting this variable every time, add the export line to your shell profile (e.g., `.bashrc` or `.zshrc`).

## Usage

Run the analysis script from the command line by providing the path to the folder you wish to analyze:
```bash
python analyze_folder_files.py /path/to/your/folder
```

The script will:
- Process each file in the folder (and its subfolders).
- Send each file's content to the Gemini LLM along with the system prompt.
- Save the aggregated results in a file named `analysis_<timestamp>.txt` (in the current directory) with each file's analysis separated by a line of equal signs.

## Project Structure

- **analyze_folder_files.py** – Main Python script.
- **requirements.txt** – Python dependencies.
- **README.md** – This documentation.

## Customization

- **System Prompt:** Edit the prompt text in `analyze_folder_files.py` if you wish to adjust the instructions given to the LLM.
- **Max Output Tokens:** Change the `max_output_tokens` parameter in the API call if longer responses are needed.
- **Error Handling:** Basic error handling is provided for file I/O and API calls.
