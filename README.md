# Kyle Language Compiler

A simple compiler/interpreter for the Kyle programming language (`.kyle` files). This is an educational project demonstrating basic interpreter implementation principles with a custom language syntax.

## Overview

This project implements a basic interpreter with:
- **Lexical Analysis** - Tokenizes Kyle source code into tokens
- **Parsing** - Builds Abstract Syntax Tree (AST) using recursive descent
- **Interpretation** - Executes AST nodes with environment management
- **Type System** - Simple typing with custom token and AST node definitions
- **File Processing** - Direct execution of `.kyle` files with validation

## Architecture

### Core Components

1. **Lexer** (`lexer/lexer.py`) - Basic tokenizer using StreamIterator
2. **Parser** (`parser/parser.py`) - Recursive descent parser with dispatch tables
3. **Interpreter** (`Semantics/interpreter.py`) - Simple AST execution engine
4. **Type Declarations** (`type_decl/`) - Basic token and AST node definitions
5. **Configuration** (`configurables/decl.py`) - Parser configuration and error handling
6. **Utilities** (`util/`) - Multiple utility modules including StreamIterator, I/O helpers, and parser helpers

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
# Execute a Kyle source file
python main.py sample.kyle

# Interactive interpreter mode (no arguments)
python main.py
```

**File Validation**: The compiler only accepts `.kyle` files. Files with other extensions or multiple dots will be rejected with an error message.

### Sample Code

```kyle
name = "george"
age = 21

if (age >= 18){
    builtin_print("You are an adult")
}otherwise{
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
├── main.py              # Main entry point with file validation
├── sample.kyle          # Sample Kyle source code
├── .gitignore           # Git ignore configuration
├── lexer/
│   ├── __init__.py      # Package initialization
│   └── lexer.py         # Basic tokenizer
├── parser/
│   ├── __init__.py      # Package initialization
│   ├── parser.py        # Recursive descent parser
│   └── utils.py         # Parser utilities
├── Semantics/
│   ├── __init__.py      # Package initialization
│   └── interpreter.py   # AST execution engine with function call support
├── type_decl/
│   ├── __init__.py      # Package initialization
│   ├── lexer_types.py   # TokenType enum and Token class
│   └── parser_types.py  # AST node definitions
├── configurables/
│   ├── __init__.py      # Package initialization
│   └── decl.py          # Parser configuration
├── util/
│   ├── __init__.py      # Package initialization
│   ├── facilitators.py  # StreamIterator utility
│   ├── iohelpers.py     # I/O utilities including colored output
│   └── parser_helpers.py # Parser helper functions
└── helpers/
    └── __init__.py      # Helper package initialization
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
# Test with sample Kyle file
python main.py sample.kyle

# Interactive testing
python main.py
# Then try commands like:
# cls = 32
# builtin_print(cls)
# env
# exit
```

**Note**: The compiler only accepts `.kyle` files. Test files and other extensions are ignored by git.

## Technical Achievements

- **Basic Pipeline**: Simple lexer → parser → interpreter implementation
- **Type Safety**: Basic typing throughout the pipeline
- **Error Handling**: Enhanced error reporting with colored output
- **Modular Design**: Separation of concerns across modules
- **File Validation**: Strict .kyle file extension enforcement
- **Function Call Support**: Enhanced function call interpretation with variable handling
- **Educational Value**: Demonstrates interpreter principles

## Current Status

✅ **Functional** - Basic interpreter with execution
✅ **File Processing** - Direct .kyle file execution with validation
✅ **Variable Management** - Environment handling with function call support
✅ **Function Calls** - Enhanced built-in functions with variable arguments
✅ **Control Flow** - Simple if/otherwise statements
✅ **Type System** - Basic typing
✅ **Error Handling** - Improved error reporting with colored output
✅ **I/O Utilities** - Colored console output functions

## Limitations

- **Performance**: Not optimized for production use
- **Features**: Limited language constructs
- **Error Handling**: Basic error messages (though improved with colors)
- **Type System**: Simple type checking
- **Memory**: No memory optimization
- **File Extension**: Strict enforcement may limit flexibility

## Future Enhancements

- **User-Defined Functions**: Basic function definitions
- **Loop Constructs**: Simple while/for loops
- **Data Structures**: Basic array/list support
- **Better Error Messages**: More descriptive error reporting
- **Type Checking**: Improved type validation
- **Optimization**: Basic performance improvements
- **Package Management**: Module system for larger programs

## License

Educational project demonstrating basic interpreter implementation.
