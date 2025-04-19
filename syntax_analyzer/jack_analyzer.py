"""This module is used to parse input jack files into output xml files"""
import sys
import os

class JackAnalyzer:

    def __init__(self):
        pass

    def open_dir(self):
        input_dir = sys.argv[1]
        print(f"Printing input dir{input_dir}")
        file_paths = [f"{input_dir}/{file_name}" for file_name in os.listdir(input_dir)]
        for file in file_paths[0:1]:
            with open(file) as jack_file:
                for line in jack_file:
                    print(line)

if __name__ == '__main__':
    jack_analyzer_cls = JackAnalyzer()
    jack_analyzer_cls.open_dir()
