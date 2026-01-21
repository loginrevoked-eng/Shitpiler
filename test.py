#!/usr/bin/env python3
"""
Real-time Interpreter Demo
Shows how the compiler converts source code to Python and executes it
"""

from lexer import Lexer
from parser import Parser
from Semantics import Interpreter
import sys
import time




TradeMark = """
Author: kyle monroe
email: loginrevoked@gmail.com\n
[ Shitpiler v0.0.1- yet to be released ]
\nDESCRIPTION:
    A high-latency, low-efficiency compiler
    built for maximum disgust and gags (  please dont look at the source code :-(  ).
\n'It works on my machine, so it's a you problem.'\n
"""

def demonstrate_interpretation(filename):
    """Demonstrate the complete interpretation process"""
    print("=" * 60)
    print(f"REAL-TIME INTERPRETER DEMO: {filename}")
    print("=" * 60)
    
    # Read source code
    with open(filename, "r") as f:
        source_code = f.read()
    
    print(f"\nSOURCE CODE:")
    print("-" * 40)
    print(source_code)
    
    # Lexical Analysis
    print(f"\nLEXICAL ANALYSIS:")
    print("-" * 40)
    lexer = Lexer(source_code)
    tok_iter, tokens = lexer.tokenize()
    
    token_count = 0
    while tok_iter.has_next():
        token = tok_iter.current()
        print(f"  {token}")
        token_count += 1
        tok_iter.next()
    
    print(f"\nGenerated {token_count} tokens")
    
    # Parsing
    print(f"\nPARSING (Building AST):")
    print("-" * 40)
    parser = Parser(tokens)
    start_time = time.time()
    program = parser.parse()
    parse_time = time.time() - start_time
    
    print(f"AST built in {parse_time:.4f} seconds")
    
    # Show AST structure
    print(f"\nABSTRACT SYNTAX TREE:")
    print("-" * 40)
    for i, stmt in enumerate(program.Toplevel, 1):
        print(f"  {i}. {stmt}")
    
    # Interpretation (Real-time execution)
    print(f"\nREAL-TIME EXECUTION:")
    print("-" * 40)
    interpreter = Interpreter()
    
    print("Executing program...")
    start_time = time.time()
    result = interpreter.interpret(program)
    exec_time = time.time() - start_time
    
    print(f"Program executed in {exec_time:.4f} seconds")
    
    # Show environment state
    print(f"\nENVIRONMENT STATE:")
    print("-" * 40)
    for var, value in interpreter.environment.items():
        if not var.startswith('builtin_'):
            print(f"  {var} = {value} ({type(value).__name__})")
    
    print(f"\nDEMONSTRATION COMPLETE!")
    print("=" * 60)

def interactive_mode():
    """Interactive interpreter mode"""
    print(TradeMark)
    print("Enter 'exit' to quit, 'help' for commands")
    print("-" * 40)
    
    interpreter = Interpreter()
    
    while True:
        try:
            code = input(">>> ")
            
            if code.lower() == 'exit':
                break
            elif code.lower() == 'help':
                print("Available commands:")
                print("  exit  - Exit interactive mode")
                print("  help  - Show this help")
                print("  env   - Show environment variables")
                print("  clear - Clear environment")
                continue
            elif code.lower() == 'env':
                print("Environment:")
                for var, value in interpreter.environment.items():
                    print(f"  {var} = {value}")
                continue
            elif code.lower() == 'clear':
                interpreter = Interpreter()
                print("Environment cleared")
                continue
            
            # Lex, parse, and interpret the code
            lexer = Lexer(code)
            tok_iter, tokens = lexer.tokenize()
            
            parser = Parser(tokens)
            program = parser.parse()
            
            result = interpreter.interpret(program)
            
            if result:
                print(f"Result: {result}")
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # File mode
        demonstrate_interpretation(sys.argv[1])
    else:
        # Interactive mode
        interactive_mode()
