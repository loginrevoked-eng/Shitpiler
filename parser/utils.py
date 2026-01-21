# Parser utilities - this file is now minimal
# All core functionality has been moved to appropriate modules:
# - AST nodes: type_decl/parser_types.py
# - Token types: type_decl/lexer_types.py  
# - StreamIterator: util/facilitators.py
# - Parser configuration: configurables/decl.py
# - Error handling: configurables/decl.py

# Import the moved components for backward compatibility
from type_decl.parser_types import *
from type_decl.lexer_types import *
from util.facilitators import StreamIterator
from configurables.decl import *
