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

    ## This is just a mock function on how the flow will run
    def manipulate_files(self):
        """
        Opens a directory containing files.
        """
        # Input dir specified in 2 sys arg
        input_dir = sys.argv[1]
        # Creates paths for the files
        file_paths = [f"{input_dir}/{file_name}" for file_name in os.listdir(input_dir)]
        # Loops over files
        for file in file_paths[0:1]:
            token_types = self.open_file(file)
            dir_path = "xml_files"
            if not os.path.isdir(dir_path):
                os.makedirs(dir_path)

            _, file_name_type = file.split("/")
            file_name, _ = os.path.splitext(file_name_type)
            file_path = f"{dir_path}/{file_name}.xml"
            self.create_xml_file(file_path, token_types)

    def open_file(self, file):
        with open(file) as jack_file:
            # Tokenizes files
            token_types = self.tokenizer(jack_file)
        return token_types

    def tokenizer(self, file: str) -> dict:
        """
        Tokenizes file while adding symbol types.

        Args:
            file (str): Opened file

        Returns:
            file_struc (dict): Dict containing the tokens with symbols
        """
        file_struc = {}
        # Loop over lines in a file
        for index, line in enumerate(file):
            # Get rid of trailing whitespaces
            line_striped = line.strip()

            # Check if line doesnt contain code
            if line_striped.startswith(("//", "/*", "*/", "*")) or len(line_striped) == 0:
                continue
            # Gets the token types for the specified line
            token_types = self.tokenizer_cls.tokenize_line(line_striped)
            # Adds the token types to the dict
            file_struc[f"line_num_{index}"] = token_types

        return file_struc
    
    def create_xml_file(self, output_path: str, content: str):
        """
        Creates an XML file and writes content to it.
    
        Args:
            output_path (str): The path where the XML file will be created.
            content (str): The XML content to write to the file.
        """
        with open(output_path, "w") as xml_file:
            xml_file.write(content)


if __name__ == '__main__':
    jack_analyzer_cls = JackAnalyzer()
    jack_analyzer_cls.manipulate_files()
