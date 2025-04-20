"""File containing types for configuration"""
###############################
#  Definition for tokenizer
###############################
keywords = [
    "class",
    "constructor",
    "function",
    "method",
    "field",
    "static",
    "var",
    "int",
    "char",
    "boolean",
    "void",
    "true",
    "false",
    "null",
    "this",
    "let",
    "do",
    "if",
    "else",
    "while",
    "return"
]

symbols = [
    "{",
    "}",
    "(",
    ")",
    "[",
    "]",
    ".",
    ",",
    ";",
    "+",
    "-",
    "*",
    "/",
    "&",
    "|",
    "<",
    ">",
    "=",
    "~"
]

###############################
#  Definition for comp engine
###############################

## Statements

jack_grammar = {
    # --- Statements ---
    "statements": ["statement*"],

    "statement": [
        "letStatement",
        "ifStatement",
        "whileStatement",
        "doStatement",
        "returnStatement"
    ],

    "letStatement": [
        "'let'",
        "varName",
        ["'[', expression, ']'"],
        "'='",
        "expression",
        "';'"
    ],

    "ifStatement": [
        "'if'", "'('", "expression", "')'",
        "'{'", "statements", "'}'",
        ["'else'", "'{'", "statements", "'}'"]
    ],

    "whileStatement": [
        "'while'", "'('", "expression", "')'",
        "'{'", "statements", "'}'"
    ],

    "doStatement": [
        "'do'", "subroutineCall", "';'"
    ],

    "returnStatement": [
        "'return'", ["expression"], "';'"
    ],

    # --- Class Declarations ---
    "class": [
        "'class'", "className", "'{'",
        "classVarDec*", "subroutineDec*",
        "'}'"
    ],

    "classVarDec": [
        "('static' | 'field')",
        "type",
        "varName", "(',', varName)*",
        "';'"
    ],

    "type": [
        "'int'", "'char'", "'boolean'", "className"
    ],

    "subroutineDec": [
        "('constructor' | 'function' | 'method')",
        "('void' | type)",
        "subroutineName",
        "'('", "parameterList", "')'",
        "subroutineBody"
    ],

    "parameterList": [
        ["(type varName)", "(',', type varName)*"]
    ],

    "subroutineBody": [
        "'{'", "varDec*", "statements", "'}'"
    ],

    "varDec": [
        "'var'", "type", "varName", "(',', varName)*", "';'"
    ],

    "className": ["identifier"],
    "subroutineName": ["identifier"],
    "varName": ["identifier"],

    # --- Expression Declarations ---

    "expression": [
        "term", 
        "((op term)*)"
    ],

    "term": [
        "integerConstant", 
        "stringConstant", 
        "keywordConstant", 
        "varName", 
        "varName '[' expression ']'",
        "subroutineCall",
        "'(' expression ')'",
        "unaryOp term"
    ],

    "subroutineCall": [
        "subroutineName '(' expressionList ')'",
        "(className | varName) '.' subroutineName '(' expressionList ')'"
    ],

    "expressionList": [
        ["expression", "(',', expression)*"]
    ],

    "op": ["'+'", "'-'", "'*'", "'/'", "'&'", "'|'", "'<'", "'>'", "'='"],

    "unaryOp": ["'-'", "'~'"],

    "keywordConstant": ["'true'", "'false'", "'null'", "'this'"],

    "integerConstant": ["int"],  
    "stringConstant": ["string"]
}
