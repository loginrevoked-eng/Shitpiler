from __future__ import annotations
from typing import Any, Dict, List, Union
from type_decl.parser_types import *
from type_decl.lexer_types import TokenType
import builtins

class Interpreter:
    def __init__(self):
        self.environment: Dict[str, Any] = {}
        self.setup_builtins()
    
    def setup_builtins(self):
        """Setup built-in functions"""
        self.environment['builtin_print'] = self.builtin_print
        self.environment['builtin_input'] = input
        self.environment['builtin_len'] = len
        self.environment['builtin_str'] = str
        self.environment['builtin_int'] = int
        self.environment['builtin_float'] = float
    
    def builtin_print(self, *args):
        """Custom print function that handles our types"""
        output = []
        for arg in args:
            output.append(str(arg))
        print(" ".join(output))
    
    def interpret(self, program: ProgramNode) -> Any:
        """Interpret the entire program"""
        if not program.Toplevel:
            return None
        
        results = []
        for stmt in program.Toplevel:
            result = self.interpret_statement(stmt)
            if result is not None:
                results.append(result)
        
        return results if results else None
    
    def interpret_statement(self, stmt: Any) -> Any:
        """Interpret a single statement"""
        if isinstance(stmt, AssignmentNode):
            return self.interpret_assignment(stmt)
        elif isinstance(stmt, IfNode):
            return self.interpret_if(stmt)
        elif isinstance(stmt, FunctionCallNode):
            return self.interpret_function_call(stmt)
        elif isinstance(stmt, str) and stmt.startswith("FunctionCall"):
            return self.interpret_function_call_string(stmt)
        elif isinstance(stmt, list):
            # Handle nested statement lists
            results = []
            for s in stmt:
                result = self.interpret_statement(s)
                if result is not None:
                    results.append(result)
            return results if results else None
        else:
            raise ValueError(f"Unknown statement type: {type(stmt)}")
    
    def interpret_assignment(self, stmt: AssignmentNode) -> Any:
        """Interpret assignment statement"""
        # Extract variable name from the token
        var_name = stmt.lhs.value if hasattr(stmt.lhs, 'value') else str(stmt.lhs)
        var_name = var_name.replace("Token(TokenType.IDENTIFIER, '", "").replace("')", "")
        
        # Interpret the right-hand side
        value = self.interpret_expression(stmt.rhs)
        
        # Store in environment
        self.environment[var_name] = value
        
        return value
    
    def interpret_if(self, stmt: IfNode) -> Any:
        """Interpret if statement"""
        # Evaluate condition
        condition_result = self.interpret_condition(stmt.condition)
        
        if condition_result:
            # Execute then branch
            return self.interpret_statement(stmt.then_branch)
        elif stmt.else_branch:
            # Execute else branch
            return self.interpret_statement(stmt.else_branch)
        
        return None
    
    def interpret_condition(self, condition: str) -> bool:
        """Interpret condition expression"""
        if condition.startswith("Comparison"):
            # Parse comparison like "Comparison(age >= IntegerNode(value='18'))"
            # Extract left operand, operator, and right operand
            import re
            match = re.match(r"Comparison\(([^ ]+) ([^ ]+) (.+)\)", condition)
            if match:
                left, op, right = match.groups()
                
                # Evaluate left operand
                left_val = self.interpret_expression(left)
                
                # Evaluate right operand
                right_val = self.interpret_expression(right)
                
                # Perform comparison
                if op == ">=":
                    return left_val >= right_val
                elif op == "<=":
                    return left_val <= right_val
                elif op == ">":
                    return left_val > right_val
                elif op == "<":
                    return left_val < right_val
                elif op == "==":
                    return left_val == right_val
                elif op == "!=":
                    return left_val != right_val
                else:
                    raise ValueError(f"Unknown comparison operator: {op}")
        
        # Simple boolean expression
        return bool(self.interpret_expression(condition))
    
    def interpret_expression(self, expr: Any) -> Any:
        """Interpret expression"""
        if isinstance(expr, str):
            # Check if it's a variable name
            if expr in self.environment:
                return self.environment[expr]
            # Check if it's a string literal
            elif expr.startswith('"') and expr.endswith('"'):
                return expr[1:-1]  # Remove quotes
            # Check if it's an IntegerNode representation
            elif expr.startswith("IntegerNode"):
                import re
                match = re.search(r"value='(\d+)'", expr)
                if match:
                    return int(match.group(1))
            # Check if it's a StringNode representation
            elif expr.startswith("StringNode"):
                import re
                match = re.search(r"value='([^']*)'", expr)
                if match:
                    return match.group(1)
            # Check if it's a FloatNode representation
            elif expr.startswith("FloatNode"):
                import re
                match = re.search(r"value='([\d.]+)'", expr)
                if match:
                    return float(match.group(1))
            else:
                # Return the string as-is for variable names
                return expr
        elif hasattr(expr, 'value'):
            # Handle AST nodes like IntegerNode, StringNode
            return expr.value
        else:
            return expr

    def interpret_function_call(self, call_node: FunctionCallNode) -> Any:
        """Interpret function call from AST node"""
        # Evaluate arguments
        args = []
        for arg in call_node.args:
            if isinstance(arg, str):
                # Check if it's a variable name in the environment
                if arg in self.environment:
                    args.append(self.environment[arg])
                else:
                    # Handle literal values
                    interpreted_arg = self.interpret_expression(arg)
                    args.append(interpreted_arg)
            else:
                # Handle AST nodes
                interpreted_arg = self.interpret_expression(arg)
                args.append(interpreted_arg)
        
        # Call the function
        if call_node.name in self.environment:
            return self.environment[call_node.name](*args)
        else:
            raise NameError(f"Function '{call_node.name}' is not defined")

    def interpret_function_call_string(self, call_str: str) -> Any:
        """Interpret function call from string representation"""
        # Parse function call like "FunctionCall(builtin_print, args=[StringNode(value='You are an adult')])"
        import re
        
        match = re.match(r"FunctionCall\(([^,]+), args=\[(.*)\]\)", call_str)
        if match:
            func_name, args_str = match.groups()
            
            # Clean up function name
            func_name = func_name.strip()
            
            # Parse arguments
            args = []
            if args_str.strip():
                # Handle simple variable references
                arg_parts = args_str.split(", ")
                for arg in arg_parts:
                    # Check if it's a variable name in the environment
                    if arg.strip() in self.environment:
                        args.append(self.environment[arg.strip()])
                    else:
                        # Handle literal values
                        interpreted_arg = self.interpret_expression(arg)
                        args.append(interpreted_arg)
            
            # Call the function
            if func_name in self.environment:
                return self.environment[func_name](*args)
            else:
                raise NameError(f"Function '{func_name}' is not defined")
        
        return None
