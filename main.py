from lexer import Lexer
from parser import Parser
from Semantics import Interpreter
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <filename>")
        return
    
    with open(sys.argv[1], "r") as f:
        data = f.read()
    
    # Lexical analysis
    lexer = Lexer(data)
    tok_iter, tokens = lexer.tokenize()
    
    print("--- Tokens ---")
    while tok_iter.has_next():
        print(tok_iter.current())
        tok_iter.next()
    
    # Parsing
    print("\n--- Parsing ---")
    parser = Parser(tokens)
    program = parser.parse()
    
    # Print AST structure
    print("\n--- AST Structure ---")
    print("\n\n".join(str(stmt) for stmt in program.Toplevel))
    
    # Interpretation (Real-time execution)
    print("\n--- Execution ---")
    interpreter = Interpreter()
    result = interpreter.interpret(program)
    
    if result:
        print(f"\nProgram completed with results: {result}")
    else:
        print("\nProgram completed successfully")

if __name__ == "__main__":
    main()