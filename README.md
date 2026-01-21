# Kyle Language Compiler

A simple interpreter for the Kyle programming language (`.kyle` files).

## Overview

- **Lexical Analysis** - Tokenizes source code
- **Parsing** - Builds AST using recursive descent
- **Interpretation** - Executes AST nodes
- **Type System** - Basic token and AST node definitions
- **File Processing** - Direct execution of `.kyle` files

## Architecture

### Components

1. **Lexer** (`lexer/lexer.py`) - Tokenizer using StreamIterator
2. **Parser** (`parser/parser.py`) - Recursive descent parser
3. **Interpreter** (`Semantics/interpreter.py`) - AST execution engine
4. **Type Declarations** (`type_decl/`) - Token and AST node definitions
5. **Configuration** (`configurables/decl.py`) - Parser configuration
6. **Utilities** (`util/`) - StreamIterator, I/O helpers, parser helpers

## Language Features

### Supported Constructs
- **Variables**: `name = "Alice"`, `age = 25`
- **Data Types**: Strings, Integers, Floats
- **Control Flow**: `if/otherwise` statements
- **Functions**: Basic built-in functions
- **Expressions**: Comparison operations (`>=`, `<=`, `==`, `!=`, `>`, `<`)
- **Function Calls**: `builtin_print("message")`, `builtin_print(variable)`

### Built-in Functions
- `builtin_print` - Print function
- `builtin_input` - Input function
- `builtin_len`, `builtin_str`, `builtin_int`, `builtin_float` - Type conversion

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
├── main.py
├── sample.kyle
├── .gitignore
├── lexer/
│   ├── __init__.py
│   └── lexer.py
├── parser/
│   ├── __init__.py
│   ├── parser.py
│   └── utils.py
├── Semantics/
│   ├── __init__.py
│   └── interpreter.py
├── type_decl/
│   ├── __init__.py
│   ├── lexer_types.py
│   └── parser_types.py
├── configurables/
│   ├── __init__.py
│   └── decl.py
├── util/
│   ├── __init__.py
│   ├── facilitators.py
│   ├── iohelpers.py
│   └── parser_helpers.py
└── helpers/
    └── __init__.py
```

## Development

### Adding Features

1. Define token types in `type_decl/lexer_types.py`
2. Create AST nodes in `type_decl/parser_types.py`
3. Implement parser methods in `parser/parser.py`
4. Add interpreter logic in `Semantics/interpreter.py`
5. Update dispatch tables in `configurables/decl.py`

### Testing

```bash
# Test with sample file
python main.py sample.kyle

# Interactive mode
python main.py
```

## Technical Details

- Basic lexer → parser → interpreter pipeline
- Type safety throughout the pipeline
- Error handling with colored output
- Modular design with separated concerns
- File validation for .kyle extensions
- Function call interpretation with variable handling

## Status

✅ Functional interpreter
✅ File processing with validation
✅ Variable management
✅ Function calls
✅ Control flow
✅ Type system
✅ Error handling
✅ I/O utilities

## Limitations

- Not optimized for production
- Limited language constructs
- Basic error messages
- Simple type checking
- No memory optimization
- Strict file extension enforcement

## Future Enhancements

- User-defined functions
- Loop constructs
- Data structures
- Better error messages
- Improved type checking
- Performance optimizations
- Package management

## License

Educational project.
