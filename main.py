#!/usr/bin/env python3
"""
Real-time Interpreter Demo
Shows how the compiler converts source code to Python and executes it
"""

from lexer import Lexer
from parser import Parser
from Semantics import Interpreter, interpreter
from util.iohelpers import fmt_c
import sys
import os


INDENT = " " * 4
SUPPORTED_FILE_EXTENSION = ".kyle"
EXAMPLE_FILENAME = "kyle-is-cool{}".format(SUPPORTED_FILE_EXTENSION)
TradeMark = """
Author: kyle monroe
email: loginrevoked@gmail.com\n
[ Shitpiler v0.0.1- yet to be released ]
\nDESCRIPTION:
    A high-latency, low-efficiency compiler
    built for maximum disgust and gags (  please dont look at the source code :-(  ).
\n'It works on my machine, so it's a you problem.'\n
"""

def process_file(filename):
    try:
        with open(filename, "r",encoding="utf-8") as f:
            source_code = f.read()
        try:
            lexer = Lexer(source_code)
            tok_iter, tokens = lexer.tokenize()
            
            parser = Parser(tokens)
            program = parser.parse()
            interpreter = Interpreter()
            #print(INDENT,end="",flush=True)
            result = interpreter.interpret(program)
            print(result)
        except Exception as e:
            print(f"\n{INDENT}{e}")

    except FileNotFoundError:
        print(f"{INDENT}Buddy, that file doesn't exist! give me something located in [{os.getcwd()}]")
    except Exception as e:
        print(f"{INDENT}Error processing file: {e}")

def interactive_mode():
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
        filename = sys.argv[1]
        if not filename.endswith(".kyle") or filename.count(".") > 1:
            print(f"{INDENT}Buddy, that's not a valid {fmt_c(repr(SUPPORTED_FILE_EXTENSION), 'green')} file rename it to something like < {fmt_c(repr(EXAMPLE_FILENAME), 'green')} >")
            sys.exit()
        process_file(sys.argv[1])
    else:
        interactive_mode()
