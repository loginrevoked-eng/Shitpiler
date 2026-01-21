# Real-Time Interpreter System

A complete compiler/interpreter pipeline that converts custom source code to Python equivalent and executes it in real-time.

## Architecture

### Components

1. **Lexer** (`lexer/lexer.py`) - Tokenizes source code
2. **Parser** (`parser/parser.py`) - Builds Abstract Syntax Tree (AST)
3. **Interpreter** (`Semantics/interpreter.py`) - Executes AST in real-time
4. **Type Declarations** (`type_decl/`) - Defines tokens and AST nodes
5. **Configuration** (`configurables/`) - Parser configuration

## Features

### Language Support
- **Variables**: `name = "Alice"`, `age = 25`
- **Data Types**: Strings, Integers, Floats
- **Control Flow**: `if/otherwise` statements
- **Functions**: Built-in functions (`builtin_print`, `builtin_input`, etc.)
- **Expressions**: Comparison operations (`>=`, `<=`, `==`, `!=`, `>`, `<`)

### Real-Time Execution
- **Immediate Execution**: Code is parsed and executed immediately
- **Environment Management**: Variables stored in runtime environment
- **Built-in Functions**: Access to Python's built-in functions
- **Error Handling**: Comprehensive error reporting

## Usage

### Command Line

```bash
# Execute a source file
python main.py sample.comp

# Run demonstration
python demo.py sample.comp

# Interactive mode
python demo.py
```

### Sample Code

```comp
name = "george"
age = 21

if (age >= 18) {
    builtin_print("You are an adult")
} otherwise {
    builtin_print("You are not an adult")
}
```

### Output

```
--- Tokens ---
Token(TokenType.IDENTIFIER, 'name')
Token(TokenType.ASSIGNMENT, '=')
Token(TokenType.STRING_LITERAL, 'george')
...

--- AST Structure ---
AssignmentNode(lhs='Token(TokenType.IDENTIFIER, 'name')',rhs='george')
AssignmentNode(lhs='Token(TokenType.IDENTIFIER, 'age')',rhs=21)
IfNode(condition="Comparison(age >= IntegerNode(value='18'))", ...)

--- Execution ---
You are an adult
```

## Implementation Details

### Interpreter Architecture

The interpreter uses a **Visitor Pattern** to traverse the AST:

```python
class Interpreter:
    def interpret(self, program: ProgramNode) -> Any:
        for stmt in program.Toplevel:
            self.interpret_statement(stmt)
    
    def interpret_statement(self, stmt: Any) -> Any:
        if isinstance(stmt, AssignmentNode):
            return self.interpret_assignment(stmt)
        elif isinstance(stmt, IfNode):
            return self.interpret_if(stmt)
        # ... more statement types
```

### Environment Management

Variables are stored in a dictionary-based environment:

```python
self.environment = {
    'name': 'Alice',
    'age': 25,
    'builtin_print': <function>,
    # ...
}
```

### Expression Evaluation

Expressions are evaluated recursively:

```python
def interpret_expression(self, expr: Any) -> Any:
    if isinstance(expr, str):
        if expr in self.environment:
            return self.environment[expr]  # Variable lookup
        elif expr.startswith('"'):
            return expr[1:-1]  # String literal
    # ... more expression types
```

## Performance

The interpreter demonstrates:
- **Fast Parsing**: AST built in milliseconds
- **Efficient Execution**: Direct interpretation without intermediate compilation
- **Memory Management**: Automatic garbage collection via Python

## Extending the Language

### Adding New Statement Types

1. Define AST node in `type_decl/parser_types.py`
2. Add parser method in `parser/parser.py`
3. Add interpreter method in `Semantics/interpreter.py`

### Adding New Built-in Functions

```python
def setup_builtins(self):
    self.environment['builtin_my_func'] = self.my_function

def my_function(self, *args):
    # Custom implementation
    pass
```

## File Structure

```
Compiler/
├── main.py              # Main entry point
├── demo.py              # Demonstration script
├── sample.comp          # Sample source code
├── lexer/
│   └── lexer.py         # Tokenizer
├── parser/
│   └── parser.py        # AST builder
├── Semantics/
│   ├── __init__.py
│   └── interpreter.py   # Runtime executor
├── type_decl/
│   ├── lexer_types.py   # Token definitions
│   └── parser_types.py  # AST node definitions
├── configurables/
│   └── decl.py          # Parser configuration
└── util/
    └── facilitators.py  # Utility classes
```

## Future Enhancements

- **Type System**: Static type checking
- **Functions**: User-defined functions
- **Loops**: while/for loop support
- **Arrays/Lists**: Data structure support
- **Modules**: Import/export system
- **Optimization**: Bytecode compilation

## License

This project demonstrates a complete interpreter implementation for educational purposes.
