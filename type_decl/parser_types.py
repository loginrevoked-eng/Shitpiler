from dataclasses import dataclass
from .lexer_types import TokenType

@dataclass 
class ProgramNode:
    Toplevel :any

@dataclass
class FunctionNode:
    name: str
    params: list
    body: list
    return_type: TokenType = None

@dataclass
class IfNode:
    condition: any
    then_branch: any
    else_branch: any = None

@dataclass
class WhileNode:
    condition: any
    body: any

@dataclass
class ForNode:
    init: any
    condition: any
    increment: any
    body: any

@dataclass
class ReturnNode:
    value: any = None

@dataclass
class GotoNode:
    label: str

@dataclass
class BreakNode:
    pass

@dataclass
class ContinueNode:
    pass

@dataclass
class SwitchNode:
    expression: any
    cases: list
    default_case: any = None

@dataclass
class CaseNode:
    value: any
    body: any

@dataclass
class FunctionCallNode:
    name: str
    args: list

@dataclass
class IntegerNode:
    value : int
    type : TokenType = TokenType.INTEGER
    def __repr__(self):
        return f"IntegerNode(value='{self.value}')"

@dataclass
class FloatNode:
    value : float
    type : TokenType = TokenType.FLOAT_LITERAL
    def __repr__(self):
        return f"FloatNode(value='{self.value}')"

@dataclass
class StringNode:
    value : str
    type : TokenType = TokenType.STRING_LITERAL
    def __repr__(self):
        return f"StringNode(value='{self.value}')"

class AssignmentNode:
    def __init__(self, lvalue, lvalue_type, rvalue, rvalue_type):
        self.lhs = lvalue
        self.rhs = rvalue
        self.enforce_type(lvalue_type, rvalue_type)
    def enforce_type(self, lhs_type, rhs_type):
        if lhs_type != rhs_type and lhs_type != TokenType.IDENTIFIER:#IDENTIFIER is the required lvalue that will hold the mem address in the heap for the assigned rhs
            raise TypeError(
                f"Can't assign value from type '{rhs_type}'"
                f"to an identifier of type {lhs_type}"
            )
        else:pass
    def process(self):
        pass
    def __repr__(self):
        return f"AssignmentNode(lhs='{repr(self.lhs)}',rhs={repr(self.rhs)})"