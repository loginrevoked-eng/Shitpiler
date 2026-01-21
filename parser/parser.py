from configurables.decl import *
from type_decl.parser_types import *
from util.facilitators import StreamIterator

        

class Parser:
    def __init__(self, token_stream, look_up_hash_map=None, type_look_up_reference=None):
        self.data = token_stream
        self.token_stream = StreamIterator(self.data)
        self.lookup_table = self.get_parser_dispatch_hashmap()
        self.TypeReference = self.get_type_look_up_reference()
        self.errors = self.get_helper_functions("errors","unterminated_assignment")
        self.extensions = self.get_helper_functions("Sentinel","expected_next_tokens")
    
    def get_helper_functions(self, cls_=None, func_name=None):
        if not func_name:raise ValueError(f"{func_name} not specified when calling self.get_helper_functions()")
        if not cls_:cls_ = "errors"
        return { 
            f"{func_name}":globals()["Parser_extension_functions"][cls_][f"{func_name}"]
        }
    def get_parser_dispatch_hashmap(self):
        return globals()["parser_dispatch_table"]

    def get_type_look_up_reference(self):
        return globals()["type_look_up_reference"]

    def parse(self):
        self.program = ProgramNode(Toplevel=self.start_descent_recursion())
        return self.program
    
    def start_descent_recursion(self):
        statements = []
        while self.token_stream.has_next():
            # Stop if we hit a closing brace (end of block)
            if self.token_stream.current().type == TokenType.RBRACE:
                break
            
            next_parser = self.parser_dispatcher()
            if next_parser:
                stmt = next_parser()
                if stmt and stmt != "lalal":
                    statements.append(stmt)
            else:
                break
        return statements if statements else None
    
    def parser_dispatcher(self,tok=None):
        tok = tok if tok else self.token_stream.current()
        parser_name = self.lookup_table.get(tok.type.value,None)
        if not parser_name:
            raise ValueError(f"the 'Parser' is unfamiliar with the type of\n {self.token_stream.return_formatted_state()}")
        parser_reference = getattr(self, parser_name, None)
        return parser_reference if parser_reference else (
            self.raise_error(
                "value error",f"No parser method named '{parser_name}' exists !\n"
                f"Error while trying to parse {self.token_stream.return_formatted_state()}"
            )
        )
    
    def raise_error(self,err_type="run time",msg="Default Message To Halt Execution On Panic()"):
        match err_type:
            case "run time":
                raise RuntimeError(msg)
            case "value error":
                raise ValueError(msg)
            case "type error":
                raise TypeError(msg)
            case _:
                raise RuntimeError(msg)
    def parse_statment(self):
        curr = self.token_stream.current()
        match curr.type:
            case TokenType.IDENTIFIER:
                try:
                    peeked = self.token_stream.peek() 
                except StopIteration:
                    raise ValueError(
                        f"Syntax Error {self.token_stream.return_formatted_state()}"
                        "Doesnt Have lvalue"
                    )
                if peeked.type == TokenType.ASSIGNMENT:
                    self.token_stream.next()
                    return self.parse_assignment()
                elif peeked.type == TokenType.LPAREN:
                    # This is a function call
                    return self.parse_function_call()
                else:
                    raise TypeError("blablablavblabvlavlalalalalal")
            case TokenType.ASSIGNMENT:#this will never execute but its just for special unknown possibility
                self.token_stream.next()
                return self.parse_assignment()
            case _:
                raise TypeError(
                    "Couldn't Parse Token Because"
                    f"{self.token_stream.return_formatted_state()}"
                    "is not a statment"
                )
    def parse_assignment(self):
        try:
            previous = self.token_stream.peek_back()#get LHS
            self.token_stream.next()#commit the "=" EQUAL token: curr token will be rhs now
        except:
            raise ValueError(
                "Can Assign To Nothing buddy: gimmi something from the Left"
                f"{self.token_stream.return_formatted_state()}"
            )
       
        if previous.type == TokenType.IDENTIFIER:
            rvalue = self.parse_expression()#get rhs
            # Handle both literal nodes and string expressions
            if hasattr(rvalue, 'type') and rvalue.type not in self.TypeReference["LITERALS"]:
                raise TypeError(
                    f"{self.token_stream.return_formatted_state()}\n"
                    "Expected an Expression or a Literal found"
                    f"{repr(rvalue.value)} which has a type of {rvalue.type}"
                )
            # Extract the actual value from the expression result
            if hasattr(rvalue, 'value'):
                actual_value = rvalue.value
                actual_type = rvalue.type
            else:
                actual_value = rvalue
                actual_type = TokenType.STRING_LITERAL if isinstance(rvalue, str) else TokenType.INTEGER
            self.token_stream.next()#commit/consume rhs now the curr char of the iterator will be whatever is next to the rhs
            return AssignmentNode(lvalue=previous,lvalue_type=previous.type, rvalue=actual_value, rvalue_type=actual_type)
        else:
            raise TypeError(f"Assigning To Non Identifier \n{self.token_stream.return_formatted_state()}")

    def parse_condition(self):
        # Parse a complete condition expression (e.g., "age >= 18")
        left = self.parse_expression()
        self.token_stream.next()  # consume the left operand
        
        # Check if there's a comparison operator
        if (self.token_stream.has_next() and 
            self.token_stream.current().type in [TokenType.GREATER, TokenType.LESS, TokenType.GREATER_EQUAL, 
                                              TokenType.LESS_EQUAL, TokenType.EQUAL, TokenType.NOT_EQUAL]):
            operator = self.token_stream.current()
            self.token_stream.next()  # consume operator
            right = self.parse_expression()
            self.token_stream.next()  # consume right operand
            return f"Comparison({left} {operator.value} {right})"
        else:
            return left

    def parse_expression(self):
        curr = self.token_stream.current()
        if not curr:self.raise_error("value error",
            f'{self.errors["unterminated_assignment"](self)}'
        )
        
        # Handle simple expressions: literal, identifier, or comparison
        if curr.type in self.TypeReference["LITERALS"]:
            if curr.type == TokenType.STRING_LITERAL:
                return StringNode(value=curr.value)
            elif curr.type == TokenType.INTEGER:
                return IntegerNode(value=curr.value)
            elif curr.type == TokenType.FLOAT_LITERAL:
                return FloatNode(value=curr.value)
        elif curr.type == TokenType.IDENTIFIER:
            # Just return the identifier value
            return curr.value
        else:
            raise RuntimeError(
                f"Expressions of type {curr.type} are not implemented yet"
            )

    def parse_function(self):
        self.token_stream.next()  # consume 'fun'
        
        # Parse function name
        if not self.token_stream.has_next() or self.token_stream.current().type != TokenType.IDENTIFIER:
            self.raise_error("value error", "Expected function name after 'fun'")
        
        func_name = self.token_stream.current().value
        self.token_stream.next()  # consume function name
        
        # Parse parameters
        if not self.token_stream.has_next() or self.token_stream.current().type != TokenType.LPAREN:
            self.raise_error("value error", "Expected '(' after function name")
        
        self.token_stream.next()  # consume '('
        params = []
        
        # Parse parameter list
        while self.token_stream.has_next() and self.token_stream.current().type != TokenType.RPAREN:
            if self.token_stream.current().type == TokenType.IDENTIFIER:
                params.append(self.token_stream.current().value)
                self.token_stream.next()
                
                # Check for comma separator
                if self.token_stream.has_next() and self.token_stream.current().type == TokenType.COMMA:
                    self.token_stream.next()
            else:
                self.raise_error("value error", "Expected parameter name in function definition")
        
        if not self.token_stream.has_next() or self.token_stream.current().type != TokenType.RPAREN:
            self.raise_error("value error", "Expected ')' to close parameter list")
        
        self.token_stream.next()  # consume ')'
        
        # Parse function body
        if not self.token_stream.has_next() or self.token_stream.current().type != TokenType.LBRACE:
            self.raise_error("value error", "Expected '{' to start function body")
        
        self.token_stream.next()  # consume '{'
        
        body = []
        while self.token_stream.has_next() and self.token_stream.current().type != TokenType.RBRACE:
            stmt = self.start_descent_recursion()
            if stmt:
                body.append(stmt)
        
        if not self.token_stream.has_next() or self.token_stream.current().type != TokenType.RBRACE:
            self.raise_error("value error", "Expected '}' to close function body")
        
        self.token_stream.next()  # consume '}'
        
        return FunctionNode(name=func_name, params=params, body=body)

    def parse_if_statement(self):
        self.token_stream.next()  # consume 'if'
        
        # Parse condition
        if not self.token_stream.has_next() or self.token_stream.current().type != TokenType.LPAREN:
            self.raise_error("value error", "Expected '(' after 'if'")
        
        self.token_stream.next()  # consume '('
        condition = self.parse_condition()
        
        if not self.token_stream.has_next() or self.token_stream.current().type != TokenType.RPAREN:
            self.raise_error("value error", "Expected ')' after if condition")
        
        self.token_stream.next()  # consume ')'
        
        # Parse then branch
        if not self.token_stream.has_next() or self.token_stream.current().type != TokenType.LBRACE:
            self.raise_error("value error", "Expected '{' to start if body")
        
        self.token_stream.next()  # consume '{'
        
        then_branch = []
        while self.token_stream.has_next() and self.token_stream.current().type != TokenType.RBRACE:
            stmt = self.start_descent_recursion()
            if stmt:
                then_branch.append(stmt)
        
        if not self.token_stream.has_next() or self.token_stream.current().type != TokenType.RBRACE:
            self.raise_error("value error", "Expected '}' to close if body")
        
        self.token_stream.next()  # consume '}'
        
        # Parse else branch (otherwise)
        else_branch = None
        if (self.token_stream.has_next() and 
            self.token_stream.current().type == TokenType.OTHERWISE):
            
            self.token_stream.next()  # consume 'otherwise'
            
            if not self.token_stream.has_next() or self.token_stream.current().type != TokenType.LBRACE:
                self.raise_error("value error", "Expected '{' to start otherwise body")
            
            self.token_stream.next()  # consume '{'
            
            else_branch = []
            while self.token_stream.has_next() and self.token_stream.current().type != TokenType.RBRACE:
                stmt = self.start_descent_recursion()
                if stmt:
                    else_branch.append(stmt)
            
            if not self.token_stream.has_next() or self.token_stream.current().type != TokenType.RBRACE:
                self.raise_error("value error", "Expected '}' to close otherwise body")
            
            self.token_stream.next()  # consume '}'
        
        return IfNode(condition=condition, then_branch=then_branch, else_branch=else_branch)

    def parse_function_call(self):
        # Parse function call like builtin_print("message")
        func_name = self.token_stream.current().value
        self.token_stream.next()  # consume function name
        
        if not self.token_stream.has_next() or self.token_stream.current().type != TokenType.LPAREN:
            self.raise_error("value error", "Expected '(' after function name")
        
        self.token_stream.next()  # consume '('
        args = []
        
        # Parse arguments
        while self.token_stream.has_next() and self.token_stream.current().type != TokenType.RPAREN:
            arg = self.parse_expression()
            args.append(arg)
            self.token_stream.next()  # consume the argument
            
            # Check for comma separator
            if self.token_stream.has_next() and self.token_stream.current().type == TokenType.COMMA:
                self.token_stream.next()  # consume comma
        
        if not self.token_stream.has_next() or self.token_stream.current().type != TokenType.RPAREN:
            self.raise_error("value error", "Expected ')' to close function call")
        
        self.token_stream.next()  # consume ')'
        
        return FunctionCallNode(name=func_name, args=args)

    def parse_while_statement(self):
        self.token_stream.next()  # consume 'while'
        
        # Parse condition
        if not self.token_stream.has_next() or self.token_stream.current().type != TokenType.LPAREN:
            self.raise_error("value error", "Expected '(' after 'while'")
        
        self.token_stream.next()  # consume '('
        condition = self.parse_expression()
        
        if not self.token_stream.has_next() or self.token_stream.current().type != TokenType.RPAREN:
            self.raise_error("value error", "Expected ')' after while condition")
        
        self.token_stream.next()  # consume ')'
        
        # Parse body
        if not self.token_stream.has_next() or self.token_stream.current().type != TokenType.LBRACE:
            self.raise_error("value error", "Expected '{' to start while body")
        
        self.token_stream.next()  # consume '{'
        
        body = []
        while self.token_stream.has_next() and self.token_stream.current().type != TokenType.RBRACE:
            stmt = self.start_descent_recursion()
            if stmt:
                body.append(stmt)
        
        if not self.token_stream.has_next() or self.token_stream.current().type != TokenType.RBRACE:
            self.raise_error("value error", "Expected '}' to close while body")
        
        self.token_stream.next()  # consume '}'
        
        return WhileNode(condition=condition, body=body)

    def parse_for_statement(self):
        self.token_stream.next()  # consume 'for'
        
        # Parse for loop structure
        if not self.token_stream.has_next() or self.token_stream.current().type != TokenType.LPAREN:
            self.raise_error("value error", "Expected '(' after 'for'")
        
        self.token_stream.next()  # consume '('
        
        # Parse initialization
        init = None
        if self.token_stream.has_next() and self.token_stream.current().type != TokenType.SEMICOLON:
            init = self.start_descent_recursion()
        
        if not self.token_stream.has_next() or self.token_stream.current().type != TokenType.SEMICOLON:
            self.raise_error("value error", "Expected ';' after for loop initialization")
        
        self.token_stream.next()  # consume ';'
        
        # Parse condition
        condition = None
        if self.token_stream.has_next() and self.token_stream.current().type != TokenType.SEMICOLON:
            condition = self.parse_expression()
        
        if not self.token_stream.has_next() or self.token_stream.current().type != TokenType.SEMICOLON:
            self.raise_error("value error", "Expected ';' after for loop condition")
        
        self.token_stream.next()  # consume ';'
        
        # Parse increment
        increment = None
        if self.token_stream.has_next() and self.token_stream.current().type != TokenType.RPAREN:
            increment = self.start_descent_recursion()
        
        if not self.token_stream.has_next() or self.token_stream.current().type != TokenType.RPAREN:
            self.raise_error("value error", "Expected ')' after for loop increment")
        
        self.token_stream.next()  # consume ')'
        
        # Parse body
        if not self.token_stream.has_next() or self.token_stream.current().type != TokenType.LBRACE:
            self.raise_error("value error", "Expected '{' to start for body")
        
        self.token_stream.next()  # consume '{'
        
        body = []
        while self.token_stream.has_next() and self.token_stream.current().type != TokenType.RBRACE:
            stmt = self.start_descent_recursion()
            if stmt:
                body.append(stmt)
        
        if not self.token_stream.has_next() or self.token_stream.current().type != TokenType.RBRACE:
            self.raise_error("value error", "Expected '}' to close for body")
        
        self.token_stream.next()  # consume '}'
        
        return ForNode(init=init, condition=condition, increment=increment, body=body)

    def parse_return_statement(self):
        self.token_stream.next()  # consume 'return'
        
        value = None
        if (self.token_stream.has_next() and 
            self.token_stream.current().type in self.TypeReference["LITERALS"]):
            value = self.parse_expression()
        
        return ReturnNode(value=value)

    def parse_goto_statement(self):
        self.token_stream.next()  # consume 'goto'
        
        if not self.token_stream.has_next() or self.token_stream.current().type != TokenType.IDENTIFIER:
            self.raise_error("value error", "Expected label identifier after 'goto'")
        
        label = self.token_stream.current().value
        self.token_stream.next()  # consume label
        
        return GotoNode(label=label)

    def parse_bailout_statement(self):
        self.token_stream.next()  # consume 'bailout'
        return ReturnNode(value=None)  # bailout is like return without value

    def parse_break_statement(self):
        self.token_stream.next()  # consume 'break'
        return BreakNode()

    def parse_continue_statement(self):
        self.token_stream.next()  # consume 'continue'
        return ContinueNode()

    def parse_switch_statement(self):
        self.token_stream.next()  # consume 'switch'
        
        # Parse expression
        if not self.token_stream.has_next() or self.token_stream.current().type != TokenType.LPAREN:
            self.raise_error("value error", "Expected '(' after 'switch'")
        
        self.token_stream.next()  # consume '('
        expression = self.parse_expression()
        
        if not self.token_stream.has_next() or self.token_stream.current().type != TokenType.RPAREN:
            self.raise_error("value error", "Expected ')' after switch expression")
        
        self.token_stream.next()  # consume ')'
        
        # Parse switch body
        if not self.token_stream.has_next() or self.token_stream.current().type != TokenType.LBRACE:
            self.raise_error("value error", "Expected '{' to start switch body")
        
        self.token_stream.next()  # consume '{'
        
        cases = []
        default_case = None
        
        while self.token_stream.has_next() and self.token_stream.current().type != TokenType.RBRACE:
            if (self.token_stream.current().type == TokenType.KEYWORD and 
                self.token_stream.current().value == "case"):
                
                self.token_stream.next()  # consume 'case'
                
                # Parse case value
                if not self.token_stream.has_next():
                    self.raise_error("value error", "Expected case value")
                
                case_value = self.parse_expression()
                
                # Parse case body
                body = []
                while (self.token_stream.has_next() and 
                       self.token_stream.current().type != TokenType.RBRACE and
                       not (self.token_stream.current().type == TokenType.KEYWORD and 
                            self.token_stream.current().value in ["case", "default"])):
                    stmt = self.start_descent_recursion()
                    if stmt:
                        body.append(stmt)
                
                cases.append(CaseNode(value=case_value, body=body))
                
            elif (self.token_stream.current().type == TokenType.KEYWORD and 
                  self.token_stream.current().value == "default"):
                
                self.token_stream.next()  # consume 'default'
                
                # Parse default body
                default_case = []
                while (self.token_stream.has_next() and 
                       self.token_stream.current().type != TokenType.RBRACE):
                    stmt = self.start_descent_recursion()
                    if stmt:
                        default_case.append(stmt)
            else:
                self.raise_error("value error", "Expected 'case' or 'default' in switch body")
        
        if not self.token_stream.has_next() or self.token_stream.current().type != TokenType.RBRACE:
            self.raise_error("value error", "Expected '}' to close switch body")
        
        self.token_stream.next()  # consume '}'
        
        return SwitchNode(expression=expression, cases=cases, default_case=default_case)
    def parse_case_statement(self):
        # This should never be called directly - cases are handled in parse_switch_statement
        self.raise_error("value error", "'case' statements should only appear within switch statements")

    def parse_default_statement(self):
        # This should never be called directly - default is handled in parse_switch_statement
        self.raise_error("value error", "'default' statements should only appear within switch statements")