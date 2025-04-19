"""This module is used to tokenize lines of jack code"""
import config

class JackTokenizer:
    """
    Class used to tokenize jack code
    """
    def __init__(self):
        self.curr_line = None

    def tokenize_line(self, line: str):
        """
        Tokenizes the line.

        Args:
            line (str): JACK code line

        Returns:
            token_types (list): List containing strings and their types.
        """

        # Initialize vars
        self.curr_line = line
        token_types = []
        token = ""
        
        # Loop over the current line
        for char in self.curr_line:
            # Check if the char is a symbol

            if char in config.symbols:
                if token:  # If there's a token being built, add it first
                    token_types.append(self.classify_token(token))
                    token = ""
                token_types.append({"SYMBOL": char})
            elif char.isspace():  # Handle whitespace as a token delimiter
                if token:
                    token_types.append(self.classify_token(token))
                    token = ""
            else:
                token += char  # Build the token character by character

        # Add the last token if it exists
        if token:
            token_types.append(self.classify_token(token))
    
        return token_types
    
    def classify_token(self, token: str):
        """
        Classify a token and return its type.
        """
        if token.isdigit():
            return {"INT_CONST": token}
        if token.replace('"', '').isalpha() and '"' in token:
            return {"STRING_CONST": token}
        if not token[0].isdigit():
            if token in config.keywords:
                return {"KEYWORD": token}
            return {"IDENTIFIER": token}
        return {"UNKNOWN": token}