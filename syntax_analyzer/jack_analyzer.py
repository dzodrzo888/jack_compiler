"""This module is used to parse input jack files into output xml files"""
import sys
import os
from jack_tokenizer import JackTokenizer

class JackAnalyzer:
    """
    Class used to analyze jack files and turn them into xml tree structured files.
    """
    def __init__(self):
        self.tokenizer_cls = JackTokenizer()

    def open_dir(self):
        """
        Opens a directory containing files.
        """
        # Input dir specified in 2 sys arg
        input_dir = sys.argv[1]
        # Creates paths for the files
        file_paths = [f"{input_dir}/{file_name}" for file_name in os.listdir(input_dir)]
        # Loops over files
        for file in file_paths[0:1]:
            # Opens files
            with open(file) as jack_file:
                # Tokenizes files
                self.tokenizer(jack_file)

    def tokenizer(self, file):
        """
        Returns tokenized files
        """
        file_struc = {}
        # Loop over lines in a file
        for index, line in enumerate(file):
            # Get rid of trailing whitespaces
            line_striped = line.strip()

            # Check if line doesnt contain code
            if line_striped.startswith(("//", "/*", "*/", "*")) or len(line_striped) == 0:
                continue
            else:
                token_types = self.tokenizer_cls.tokenize_line(line_striped)
                file_struc[f"line_num_{index}"] = token_types
        print(file_struc)

if __name__ == '__main__':
    jack_analyzer_cls = JackAnalyzer()
    jack_analyzer_cls.open_dir()
