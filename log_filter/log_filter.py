import os
import argparse

def filter_log(input_file, output_file, search_string):
    """
    Filters lines containing the search_string from input_file and writes them to output_file.

    Parameters:
    - input_file (str): Path to the input log file.
    - output_file (str): Path to the output file to save filtered lines.
    - search_string (str): The string to search for in each line.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            # Read all lines from the input file
            lines = infile.readlines()
        
        # Filter lines that contain the search string
        filtered_lines = [line for line in lines if search_string in line]
        
        # Write the filtered lines to the output file
        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.writelines(filtered_lines)
        
        print(f"Filtering complete. {len(filtered_lines)} lines written to '{output_file}'.")
    
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' does not exist in the current directory.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Filter log files based on search string')
    parser.add_argument('--search_str', required=True, help='String to search for in log file')
    parser.add_argument('--input', default='log.txt', help='Input log filename (default: log.txt)')
    parser.add_argument('--output', default='filtered_log.txt', help='Output filename (default: filtered_log.txt)')
    
    args = parser.parse_args()
    
    # Get the current working directory
    current_dir = os.getcwd()
    
    # Construct full paths
    input_path = os.path.join(current_dir, args.input)
    output_path = os.path.join(current_dir, args.output)
    
    # Call the filter function
    filter_log(input_path, output_path, args.search_str)

if __name__ == "__main__":
    main()
