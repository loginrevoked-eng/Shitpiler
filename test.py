from util.facilitators import StreamIterator
from dataclasses import dataclass
from enum import Enum


class TokenType(Enum):
    IDENTIFIER = "identifier"
    STRING_LITERAL = "string literal"
    INTEGER_LITERAL = "int literal"
    ASSIGNMENT = "="
    LPAREN = "(" 
    RPAREN = ")"

@dataclass
class Token:
    value : str
    type : TokenType
@dataclass
class ExprNode:
    value : Token
@dataclass
class AssignNode:
    lvalue : ExprNode
    rvalue : ExprNode


class Parser:
    def __init__(self,token_stream):
        self.tokens = token_stream
        self.token_stream = StreamIterator(self.tokens)
    def parse(self):
        curr  = self.current()
        match curr.type:
            case TokenType.IDENTIFIER:
                if self.precceds(TokenType.ASSIGNMENT):
                    self.expect(TokenType.ASSIGNMENT)
                    return AssignNode(lvalue=ExprNode(value=curr),rvalue=self.parse_expression())
            case _:
                raise Exception("Invalid syntax")
    def current(self):
        return self.token_stream.current()
    def precceds(self,token_type:TokenType):
        return self.token_stream.peek().type == token_type
    def follows(self,token_type:TokenType):
        return self.token_stream.peek_back().type == token_type
    def expect(self,*args):
        next = self.token_stream.peek()
        for type in args:
            if next.type == type:
                self.token_stream.next()
                self.token_stream.next()
                return
        raise Exception("Invalid syntax")
    def parse_expression(self):
        curr = self.current()
        match curr.type:
            case TokenType.IDENTIFIER:
                return ExprNode(value=curr)
            case TokenType.LPAREN:
                self.expect(TokenType.STRING_LITERAL, TokenType.INTEGER_LITERAL)
                curr = self.current()
                self.expect(TokenType.RPAREN)
                return ExprNode(value=curr)
            case TokenType.STRING_LITERAL:
                return ExprNode(value=curr)
            case TokenType.INTEGER_LITERAL:
                return ExprNode(value=curr)
            case _:
                raise Exception("Invalid syntax")


test = [
    Token(value="name",type=TokenType.IDENTIFIER),
    Token(value="=",type=TokenType.ASSIGNMENT),
    Token(value="george",type=TokenType.STRING_LITERAL),
]

parser = Parser(test)
print(parser.parse())
    
                    
                