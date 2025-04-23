class SymbolTable:
    """
    Manages a symbol table for Jack compilation.
    """
    def __init__(self):
        # Separate tables for class-level and subroutine-level symbols
        self.class_table = {}
        self.subroutine_table = {}
        self.index_counters = {
            "static": 0,
            "field": 0,
            "arg": 0,
            "var": 0
        }

    def start_subroutine(self):
        """
        Resets the subroutine-level symbol table.
        """
        self.subroutine_table = {}
        self.index_counters["arg"] = 0
        self.index_counters["var"] = 0

    def define(self, name, type_, kind):
        """
        Defines a new identifier and adds it to the appropriate symbol table.

        Args:
            name (str): The name of the identifier.
            type_ (str): The type of the identifier.
            kind (str): The kind of the identifier ('static', 'field', 'arg', 'var').
        """
        if kind in ["static", "field"]:
            self.class_table[name] = {"type": type_, "kind": kind, "index": self.index_counters[kind]}
        elif kind in ["arg", "var"]:
            self.subroutine_table[name] = {"type": type_, "kind": kind, "index": self.index_counters[kind]}
        else:
            raise ValueError(f"Invalid kind: {kind}")
        self.index_counters[kind] += 1

    def var_count(self, kind):
        """
        Returns the number of variables of the given kind.

        Args:
            kind (str): The kind of the variable ('static', 'field', 'arg', 'var').

        Returns:
            int: The count of variables of the given kind.
        """
        return self.index_counters[kind]

    def kind_of(self, name):
        """
        Returns the kind of the identifier.

        Args:
            name (str): The name of the identifier.

        Returns:
            str: The kind of the identifier, or None if not found.
        """
        if name in self.subroutine_table:
            return self.subroutine_table[name]["kind"]
        elif name in self.class_table:
            return self.class_table[name]["kind"]
        return None

    def type_of(self, name):
        """
        Returns the type of the identifier.

        Args:
            name (str): The name of the identifier.

        Returns:
            str: The type of the identifier, or None if not found.
        """
        if name in self.subroutine_table:
            return self.subroutine_table[name]["type"]
        elif name in self.class_table:
            return self.class_table[name]["type"]
        return None

    def index_of(self, name):
        """
        Returns the index assigned to the identifier.

        Args:
            name (str): The name of the identifier.

        Returns:
            int: The index of the identifier, or None if not found.
        """
        if name in self.subroutine_table:
            return self.subroutine_table[name]["index"]
        elif name in self.class_table:
            return self.class_table[name]["index"]
        return None