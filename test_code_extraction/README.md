This script takes in a json file from promptfoo test framework and extracts the code blocks from the json file that are written in Python.
It was used for my Thesis to automate the extraction of code from the json files that were generated while testing the prompts developed for software engineering.

To run the script with input.json and output to my_tests directory:
```bash
python main.py input.json --output-dir my_tests
```

To extract code blocks for a different language, use the `--language` flag:
```bash
python main.py input.json --output-dir my_tests --language xml --fileExtension .xml
```

Note that if there are any inconsistencies in the format that the LLM produces for the test cases, the output of the Python files will be incorrect. However, with a sophisticated prompt, the LLM can be made to produce output that is consistent and can be extracted using this script, as with the Thesis project.
