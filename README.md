# Real-Time Interpreter System

A simple compiler/interpreter pipeline that converts custom source code to Python and executes it. This is an educational project demonstrating basic interpreter implementation principles.

## Overview

This project implements a basic interpreter with:
- **Lexical Analysis** - Tokenizes source code into tokens
- **Parsing** - Builds Abstract Syntax Tree (AST) using recursive descent
- **Interpretation** - Executes AST nodes with basic environment management
- **Type System** - Simple typing with custom token and AST node definitions

## Architecture

### Core Components

1. **Lexer** (`lexer/lexer.py`) - Basic tokenizer using StreamIterator
2. **Parser** (`parser/parser.py`) - Recursive descent parser with dispatch tables
3. **Interpreter** (`Semantics/interpreter.py`) - Simple AST execution engine
4. **Type Declarations** (`type_decl/`) - Basic token and AST node definitions
5. **Configuration** (`configurables/decl.py`) - Parser configuration and error handling
6. **Utilities** (`util/facilitators.py`) - StreamIterator for navigation

## Language Features

### Supported Constructs
- **Variables**: `name = "Alice"`, `age = 25`
- **Data Types**: Strings, Integers, Floats
- **Control Flow**: `if/otherwise` statements
- **Functions**: Basic built-in functions
- **Expressions**: Simple comparison operations (`>=`, `<=`, `==`, `!=`, `>`, `<`)
- **Function Calls**: `builtin_print("message")`, `builtin_print(variable)`

### Built-in Functions
- `builtin_print` - Basic print function
- `builtin_input` - Python's input function
- `builtin_len`, `builtin_str`, `builtin_int`, `builtin_float` - Type conversion functions

## Usage

### Command Line Interface

```bash
# Execute a source file with full demonstration
python main.py sample.comp

# Interactive interpreter mode (no arguments)
python main.py
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

### Execution Pipeline

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

Environment State:
name = george (str)
age = 21 (int)
```

## Implementation Details

### Lexer Architecture

Basic lexer using **StreamIterator** pattern:
- **Token Types**: Standard TokenType enum with common tokens
- **Reserved Keywords**: Basic keyword recognition
- **Error Handling**: Simple error reporting

### Parser Architecture

Recursive descent parser with **dispatch table**:
- **Dispatch Table**: Maps token types to parser methods
- **AST Nodes**: Basic AST node hierarchy
- **Error Recovery**: Basic error handling

### Interpreter Architecture

Simple **Visitor Pattern** implementation:
- **Environment Management**: Dictionary-based variable storage
- **Type Handling**: Basic type conversion
- **Function Calls**: AST node-based function calls

### Key Classes

```python
# Basic interpreter loop
class Interpreter:
    def interpret(self, program: ProgramNode) -> Any:
        for stmt in program.Toplevel:
            self.interpret_statement(stmt)

# Simple environment management
self.environment = {
    'name': 'Alice',
    'age': 25,
    'builtin_print': <method>,
}

# Basic AST node handling
def interpret_statement(self, stmt: Any) -> Any:
    if isinstance(stmt, AssignmentNode):
        return self.interpret_assignment(stmt)
    elif isinstance(stmt, IfNode):
        return self.interpret_if(stmt)
```

## Performance Characteristics

- **Parsing Speed**: Basic AST construction
- **Execution Speed**: Simple interpretation without optimization
- **Memory Usage**: Basic Python garbage collection
- **Scalability**: Handles simple programs and expressions

## File Structure

```
Compiler/
├── main.py              # Main entry point
├── sample.comp          # Sample source code
├── test.py              # Test file
├── test_complex.comp    # Complex test file
├── .gitignore           # Git ignore configuration
├── lexer/
│   └── lexer.py         # Basic tokenizer
├── parser/
│   └── parser.py        # Recursive descent parser
├── Semantics/
│   ├── __init__.py      # Package initialization
│   └── interpreter.py   # Simple execution engine
├── type_decl/
│   ├── lexer_types.py   # TokenType enum and Token class
│   └── parser_types.py  # AST node definitions
├── configurables/
│   └── decl.py          # Parser configuration
└── util/
    └── facilitators.py  # StreamIterator utility
```

## Development Workflow

### Adding New Language Features

1. **Define Token Types** in `type_decl/lexer_types.py`
2. **Create AST Nodes** in `type_decl/parser_types.py`
3. **Implement Parser Methods** in `parser/parser.py`
4. **Add Interpreter Logic** in `Semantics/interpreter.py`
5. **Update Dispatch Tables** in `configurables/decl.py`

### Testing

```bash
# Test with sample files (full demonstration)
python main.py sample.comp

# Test with complex sample
python main.py test_complex.comp

# Interactive testing
python main.py
# Then try commands like:
# cls = 32
# builtin_print(cls)
# env
# exit
```

## Technical Achievements

- **Basic Pipeline**: Simple lexer → parser → interpreter implementation
- **Type Safety**: Basic typing throughout the pipeline
- **Error Handling**: Simple error reporting
- **Modular Design**: Separation of concerns across modules
- **Educational Value**: Demonstrates interpreter principles

## Current Status

✅ **Functional** - Basic interpreter with execution
✅ **Variable Management** - Simple environment handling
✅ **Function Calls** - Basic built-in functions
✅ **Control Flow** - Simple if/otherwise statements
✅ **Type System** - Basic typing
✅ **Error Handling** - Simple error reporting

## Limitations

- **Performance**: Not optimized for production use
- **Features**: Limited language constructs
- **Error Handling**: Basic error messages
- **Type System**: Simple type checking
- **Memory**: No memory optimization

## Future Enhancements

- **User-Defined Functions**: Basic function definitions
- **Loop Constructs**: Simple while/for loops
- **Data Structures**: Basic array/list support
- **Better Error Messages**: More descriptive error reporting
- **Type Checking**: Improved type validation
- **Optimization**: Basic performance improvements

## License

Educational project demonstrating basic interpreter implementation.
