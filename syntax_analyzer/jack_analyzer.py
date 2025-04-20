"""This module is used to parse input jack files into output xml files"""
import sys
import os
from jack_tokenizer import JackTokenizer
from jack_comp_engine import JackCompEngine

class JackAnalyzer:
    """
    Class used to analyze jack files and turn them into xml tree structured files.
    """
    def __init__(self):
        self.tokenizer_cls = JackTokenizer()
        self.comp_engine_cls = JackCompEngine()
        self.file_struc = []

    ## This is just a mock function on how the flow will run
    def manipulate_files(self):
        """
        Opens a directory containing files.
        """
        # Define dir
        dir_path = "xml_files"
        self.create_xml_dir(dir_path)
        # Input dir specified in sys arg
        input_dir = sys.argv[1]
        # Creates paths for the files
        file_paths = [f"{input_dir}/{file_name}" for file_name in os.listdir(input_dir)]
        # Loops over files
        for file in file_paths:
            with open(file) as jack_file:
                # Tokenizes files
                self.tokenizer(jack_file)
                file_name = self.get_file_name(file)
                # Set xml path
                file_path = f"{dir_path}/{file_name}.xml"
                # Open XML file for writing
                with open(file_path, "w") as xml_file:
                    self.comp_engine_cls.populate_xml(xml_file, self.file_struc)
            self.file_struc = []

    def create_xml_dir(self, dir_path):
        """
        Creates xml dir
        """
        # If path doesnt exist create it
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)

    def get_file_name(self, file) -> str:
        """
        Gets the name of the file

        Args:
            file (opened_file): Opened file

        Returns:
            file_name (str): Name of a file
        """
        # Get the file name
        _, file_name_type = file.split("/")
        file_name, _ = os.path.splitext(file_name_type)
        return file_name

    def tokenizer(self, file: str) -> dict:
        """
        Tokenizes file while adding symbol types.

        Args:
            file (str): Opened file

        Returns:
            file_struc (list): Dict containing the tokens with symbols
        """
        # Loop over lines in a file
        for line in file:
            # Get rid of trailing whitespaces
            line_striped = line.strip()

            # Check if line doesnt contain code
            if line_striped.startswith(("//", "/*", "*/", "*")) or len(line_striped) == 0:
                continue
            # Gets the token types for the specified line
            token_types = self.tokenizer_cls.tokenize_line(line_striped)
            # Adds the token types to the dict
            self.file_struc.append(token_types)

    def create_xml_file(self, output_path: str):
        """
        Creates an XML file and writes content to it.
    
        Args:
            output_path (str): The path where the XML file will be created.
            content (str): The XML content to write to the file.
        """
        with open(output_path, "w") as xml_file:
            return xml_file


if __name__ == '__main__':
    jack_analyzer_cls = JackAnalyzer()
    jack_analyzer_cls.manipulate_files()
