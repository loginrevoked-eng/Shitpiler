from dataclasses import dataclass,field
from enum import Enum








class TokenType(Enum):
    ILLEGAL_SYMBOL = "ILLEGAL_SYMBOL"
    IDENTIFIER = "IDENTIFIER"
    INTEGER = "INTEGER"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    PLUS_PLUS = "PLUS_PLUS"
    MINUS_MINUS = "MINUS_MINUS"
    PLUS_EQUAL = "PLUS_EQUAL"
    MINUS_EQUAL = "MINUS_EQUAL"
    MULTIPLY_EQUAL = "MULTIPLY_EQUAL"
    DIVIDE_EQUAL = "DIVIDE_EQUAL"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    GREATER = "GREATER"
    LESS = "LESS"
    GREATER_EQUAL = "GREATER_EQUAL"
    LESS_EQUAL = "LESS_EQUAL"
    EQUAL = "EQUAL"
    NOT_EQUAL = "NOT_EQUAL"
    TAG = "TAG"
    ANPERSAND = "ANPERSAND"
    ASSIGNMENT = "ASSIGNMENT"
    DOUBLE_ANPERSAND = "DOUBLE_ANPERSAND"
    COMMENT = "COMMENT"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    SINGLE_QUOTE = "SINGLE_QUOTE"
    DOUBLE_QUOTE = "DOUBLE_QUOTE"
    STRING_LITERAL = "STRING_LITERAL"
    FLOAT_LITERAL = "FLOAT_LITERAL"
    SEMICOLON = "SEMICOLON"
    COMMA = "COMMA"
    KEYWORD = "KEY_WORDS_RESERVED"
    BULK_COMMENT_TAG_LEFT = "/*"
    BULK_COMMENT_TAG_RIGHT = "*/"
    FUN = "FUN"
    WHILE = "WHILE"
    FOR = "FOR"
    RETURN = "RETURN"
    GOTO = "GOTO"
    BAILOUT = "BAILOUT"
    BREAK = "BREAK"
    CONTINUE = "CONTINUE"
    SWITCH = "SWITCH"
    CASE = "CASE"
    DEFAULT = "DEFAULT"
    IF = "IF"
    OTHERWISE = "OTHERWISE"


CTOT_MAP = {
    "++": TokenType.PLUS_PLUS,
    "--": TokenType.MINUS_MINUS,
    "+=": TokenType.PLUS_EQUAL,
    "-=": TokenType.MINUS_EQUAL,
    "*=": TokenType.MULTIPLY_EQUAL,
    "/=": TokenType.DIVIDE_EQUAL,
    ">=": TokenType.GREATER_EQUAL,
    "<=": TokenType.LESS_EQUAL,
    "==": TokenType.EQUAL,
    "!=": TokenType.NOT_EQUAL,
    ">": TokenType.GREATER,
    "<": TokenType.LESS,
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    "*": TokenType.MULTIPLY,
    "/": TokenType.DIVIDE,
    "(": TokenType.LPAREN,
    ")": TokenType.RPAREN,
    "#": TokenType.TAG,
    "=": TokenType.ASSIGNMENT,
    "&": TokenType.ANPERSAND,
    "&&": TokenType.DOUBLE_ANPERSAND,
    "{": TokenType.LBRACE,
    "}": TokenType.RBRACE,
    "'": TokenType.SINGLE_QUOTE,
    '"': TokenType.DOUBLE_QUOTE,
    "/*":TokenType.BULK_COMMENT_TAG_LEFT,
    "*/":TokenType.BULK_COMMENT_TAG_RIGHT,
    ";": TokenType.SEMICOLON,
    ",": TokenType.COMMA,
    "if": TokenType.IF,
    "otherwise": TokenType.OTHERWISE,
    "fun": TokenType.FUN,
    "while": TokenType.WHILE,
    "for": TokenType.FOR,
    "return": TokenType.RETURN,
    "goto": TokenType.GOTO,
    "bailout": TokenType.BAILOUT,
    "break": TokenType.BREAK,
    "continue": TokenType.CONTINUE,
    "switch": TokenType.SWITCH,
    "case": TokenType.CASE,
    "default": TokenType.DEFAULT
}


RESERVED = [
    "if","otherwise","fun","while","for","return","goto","bailout","break","continue","switch","case","default"
]




@dataclass
class LocationMetadata:
    line:int
    column:int


@dataclass
class Token:
    type: TokenType
    value: str
    location_metadata : LocationMetadata =field(
        default_factory=lambda: LocationMetadata(None, None)
    ) #will store the column/lineno of this token in the original data , the kexer should provide these metadata for the parser
    def __repr__(self):
        return f"Token({self.type}, '{self.value}')"
