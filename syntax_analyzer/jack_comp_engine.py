"""This module is used to compile the given code"""
import config

class JackCompEngine:
    """
    This class is used to compile given code.
    """
    def __init__(self):
        self.xml_file = None
        self.cls_config = None
        self.curr_token = None
        self.token_types = None

    def populate_xml(self, xml_file, token_types):
        """
        Entry point for the compilation process.
        """
        self.token_types = token_types
        self.curr_token = self.token_types[0]
        self.xml_file = xml_file
        self.compile_class()

    def compile_class(self):
        """
        Compiles a class structure.
        """
        key, value = self.get_current_token()

        # Ensure the first token is "class"
        if value != "class":
            raise SyntaxError("Expected 'class' keyword at the beginning of the class definition.")
        self.write_token(key, value)
        self.advance_token()

        # Process the class name (identifier)
        key, value = self.get_current_token()
        if key != "IDENTIFIER":
            raise SyntaxError("Expected class name (identifier).")
        self.write_token(key, value)
        self.advance_token()

        # Process the opening '{'
        key, value = self.get_current_token()
        if value != "{":
            raise SyntaxError("Expected '{' after class name.")
        self.write_token(key, value)
        self.advance_token()

        # Handle classVarDec* (zero or more class variable declarations)
        while self.get_current_token()[1] in ["static", "field"]:
            self.compile_classVarDec()

        # Handle subroutineDec* (zero or more subroutine declarations)
        while self.get_current_token()[1] in ["constructor", "function", "method"]:
            self.compile_subroutineDec()

        # Process the closing '}'
        key, value = self.get_current_token()
        if value != "}":
            raise SyntaxError("Expected '}' at the end of the class definition.")
        self.write_token(key, value)
        self.advance_token()

    def compile_classVarDec(self):
        """
        Compiles a class variable declaration.
        """
        self.xml_file.write("<classVarDec>\n")
        key, value = self.get_current_token()
        while value != ";":  # Process until the semicolon
            self.write_token(key, value)
            self.advance_token()
            key, value = self.get_current_token()
        # Write the semicolon
        self.write_token(key, value)
        self.advance_token()
        self.xml_file.write("</classVarDec>\n")

    def compile_subroutineDec(self):
        """
        Compiles a subroutine declaration.
        """
        self.xml_file.write("<subroutineDec>\n")
        key, value = self.get_current_token()
        while value != "{":  # Process until the opening '{'
            self.write_token(key, value)
            self.advance_token()
            key, value = self.get_current_token()

        # Process the subroutine body
        self.write_token(key, value)  # Write the opening '{'
        self.advance_token()
        self.compile_subroutineBody()
        self.xml_file.write("</subroutineDec>\n")

    def compile_subroutineBody(self):
        """
        Compiles a subroutine body.
        """
        self.xml_file.write("<subroutineBody>\n")
        key, value = self.get_current_token()

        # Handle varDec* (zero or more variable declarations)
        while value == "var":
            self.compile_varDec()
            key, value = self.get_current_token()

        # Handle statements
        self.compile_statements()

        # Process the closing '}'
        key, value = self.get_current_token()
        if value != "}":
            raise SyntaxError("Expected '}' at the end of the subroutine body.")
        self.write_token(key, value)
        self.advance_token()
        self.xml_file.write("</subroutineBody>\n")

    def compile_varDec(self):
        """
        Compiles a variable declaration.
        """
        self.xml_file.write("<varDec>\n")
        key, value = self.get_current_token()
        while value != ";":  # Process until the semicolon
            self.write_token(key, value)
            self.advance_token()
            key, value = self.get_current_token()
        # Write the semicolon
        self.write_token(key, value)
        self.advance_token()
        self.xml_file.write("</varDec>\n")

    def compile_statements(self):
        """
        Compiles a sequence of statements.
        """
        self.xml_file.write("<statements>\n")
        while self.get_current_token()[1] in ["let", "if", "while", "do", "return"]:
            key, value = self.get_current_token()
            if value == "let":
                self.compile_let()
            elif value == "if":
                self.compile_if()
            elif value == "while":
                self.compile_while()
            elif value == "do":
                self.compile_do()
            elif value == "return":
                self.compile_return()
        self.xml_file.write("</statements>\n")

    def compile_let(self):
        """
        Compiles a let statement.
        """
        self.xml_file.write("<letStatement>\n")
        self.process_until(";")
        self.xml_file.write("</letStatement>\n")

    def compile_if(self):
        """
        Compiles an if statement.
        """
        self.xml_file.write("<ifStatement>\n")
        self.process_until("}")
        self.xml_file.write("</ifStatement>\n")

    def compile_while(self):
        """
        Compiles a while statement.
        """
        self.xml_file.write("<whileStatement>\n")
        self.process_until("}")
        self.xml_file.write("</whileStatement>\n")

    def compile_do(self):
        """
        Compiles a do statement.
        """
        self.xml_file.write("<doStatement>\n")
        self.process_until(";")
        self.xml_file.write("</doStatement>\n")

    def compile_return(self):
        """
        Compiles a return statement.
        """
        self.xml_file.write("<returnStatement>\n")
        self.process_until(";")
        self.xml_file.write("</returnStatement>\n")

    def process_until(self, stop_token):
        """
        Processes tokens until a specific stop token is encountered.
        """
        key, value = self.get_current_token()
        while value != stop_token:
            self.write_token(key, value)
            self.advance_token()
            key, value = self.get_current_token()
        # Write the stop token
        self.write_token(key, value)
        self.advance_token()

    def compile_expression(self):
        """
        Compiles an expression.
        """
        self.xml_file.write("<expression>\n")
        self.compile_term()
        while self.get_current_token()[1] in config.jack_grammar["op"]:
            key, value = self.get_current_token()
            self.write_token(key, value)
            self.advance_token()
            self.compile_term()
        self.xml_file.write("</expression>\n")

    def compile_term(self):
        """
        Compiles a term.
        """
        self.xml_file.write("<term>\n")
        key, value = self.get_current_token()

        if value in config.jack_grammar["unaryOp"]:
            # Unary operation
            self.write_token(key, value)
            self.advance_token()
            self.compile_term()
        elif value == "(":
            # Parenthesized expression
            self.write_token(key, value)
            self.advance_token()
            self.compile_expression()
            key, value = self.get_current_token()
            if value != ")":
                raise SyntaxError("Expected ')' after expression.")
            self.write_token(key, value)
            self.advance_token()
        elif key == "INT_CONST" or key == "STRING_CONST" or value in config.jack_grammar["keywordConstant"]:
            # Integer constant, string constant, or keyword constant
            self.write_token(key, value)
            self.advance_token()
        elif key == "IDENTIFIER":
            # Variable, array, or subroutine call
            self.write_token(key, value)
            self.advance_token()
            if self.get_current_token()[1] == "[":
                # Array access
                key, value = self.get_current_token()
                self.write_token(key, value)
                self.advance_token()
                self.compile_expression()
                key, value = self.get_current_token()
                if value != "]":
                    raise SyntaxError("Expected ']' after array index.")
                self.write_token(key, value)
                self.advance_token()
            elif self.get_current_token()[1] in ["(", "."]:
                # Subroutine call
                self.compile_subroutineCall()
        else:
            raise SyntaxError(f"Unexpected term: {value}")
        self.xml_file.write("</term>\n")

    def compile_expressionList(self):
        """
        Compiles a (possibly empty) comma-separated list of expressions.
        """
        self.xml_file.write("<expressionList>\n")
        if self.get_current_token()[1] != ")":
            self.compile_expression()
            while self.get_current_token()[1] == ",":
                key, value = self.get_current_token()
                self.write_token(key, value)
                self.advance_token()
                self.compile_expression()
        self.xml_file.write("</expressionList>\n")

    def compile_subroutineCall(self):
        """
        Compiles a subroutine call.
        """
        key, value = self.get_current_token()
        self.write_token(key, value)
        self.advance_token()

        if self.get_current_token()[1] == ".":
            # Handle className or varName followed by '.'
            key, value = self.get_current_token()
            self.write_token(key, value)
            self.advance_token()
            key, value = self.get_current_token()
            if key != "IDENTIFIER":
                raise SyntaxError("Expected subroutine name after '.'.")
            self.write_token(key, value)
            self.advance_token()

        # Handle '(' expressionList ')'
        key, value = self.get_current_token()
        if value != "(":
            raise SyntaxError("Expected '(' before expression list.")
        self.write_token(key, value)
        self.advance_token()
        self.compile_expressionList()
        key, value = self.get_current_token()
        if value != ")":
            raise SyntaxError("Expected ')' after expression list.")
        self.write_token(key, value)
        self.advance_token()

    def get_current_token(self):
        """
        Returns the current token as a (key, value) tuple.
        """
        return next(iter(self.curr_token.items()))

    def write_token(self, key, value):
        """
        Writes the current token to the XML file.
        """
        self.xml_file.write(f"<{key}> {value} </{key}>\n")

    def advance_token(self):
        """
        Advances to the next token.
        """
        if self.token_types:
            self.curr_token = self.token_types.pop(0)
        else:
            self.curr_token = None