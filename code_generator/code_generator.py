class CodeGenerator:
    """
    Generates VM code from the parsed XML structure.
    """
    def __init__(self):
        self.output = []

    def write_push(self, segment, index):
        """
        Writes a push command.

        Args:
            segment (str): The memory segment.
            index (int): The index within the segment.
        """
        self.output.append(f"push {segment} {index}")

    def write_pop(self, segment, index):
        """
        Writes a pop command.

        Args:
            segment (str): The memory segment.
            index (int): The index within the segment.
        """
        self.output.append(f"pop {segment} {index}")

    def write_arithmetic(self, command):
        """
        Writes an arithmetic command.

        Args:
            command (str): The arithmetic command.
        """
        self.output.append(command)

    def write_label(self, label):
        """
        Writes a label command.

        Args:
            label (str): The label name.
        """
        self.output.append(f"label {label}")

    def write_goto(self, label):
        """
        Writes a goto command.

        Args:
            label (str): The label name.
        """
        self.output.append(f"goto {label}")

    def write_if(self, label):
        """
        Writes an if-goto command.

        Args:
            label (str): The label name.
        """
        self.output.append(f"if-goto {label}")

    def write_call(self, name, n_args):
        """
        Writes a call command.

        Args:
            name (str): The function name.
            n_args (int): The number of arguments.
        """
        self.output.append(f"call {name} {n_args}")

    def write_function(self, name, n_locals):
        """
        Writes a function command.

        Args:
            name (str): The function name.
            n_locals (int): The number of local variables.
        """
        self.output.append(f"function {name} {n_locals}")

    def write_return(self):
        """
        Writes a return command.
        """
        self.output.append("return")

    def get_output(self):
        """
        Returns the generated VM code.

        Returns:
            list: The VM code as a list of strings.
        """
        return self.output