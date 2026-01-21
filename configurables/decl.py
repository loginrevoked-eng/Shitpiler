from type_decl.lexer_types import TokenType

#function map for each type of encountered token
parser_dispatch_table = {
    f"{TokenType.EQUAL.value}":"parse_assignment",
    f"{TokenType.IDENTIFIER.value}":"parse_statment",
    f"{TokenType.STRING_LITERAL.value}":"parse_expression",
    f"{TokenType.INTEGER.value}":"parse_expression",
    f"{TokenType.FLOAT_LITERAL.value}":"parse_expression",
    f"{TokenType.FUN.value}":"parse_function",
    f"{TokenType.IF.value}":"parse_if_statement",
    f"{TokenType.WHILE.value}":"parse_while_statement",
    f"{TokenType.FOR.value}":"parse_for_statement",
    f"{TokenType.RETURN.value}":"parse_return_statement",
    f"{TokenType.GOTO.value}":"parse_goto_statement",
    f"{TokenType.BAILOUT.value}":"parse_bailout_statement",
    f"{TokenType.BREAK.value}":"parse_break_statement",
    f"{TokenType.CONTINUE.value}":"parse_continue_statement",
    f"{TokenType.SWITCH.value}":"parse_switch_statement",
    f"{TokenType.CASE.value}":"parse_case_statement",
    f"{TokenType.DEFAULT.value}":"parse_default_statement",
}


#type infering for generalization judgements of token types
type_look_up_reference = {
    "LITERALS":[TokenType.INTEGER,TokenType.STRING_LITERAL, TokenType.FLOAT_LITERAL],
    "OPERATORS":[TokenType.EQUAL],
    "KEYWORDS":[TokenType.FUN, TokenType.IF, TokenType.WHILE, TokenType.FOR, TokenType.RETURN, 
               TokenType.GOTO, TokenType.BAILOUT, TokenType.BREAK, TokenType.CONTINUE, 
               TokenType.SWITCH, TokenType.CASE, TokenType.DEFAULT],
    "CONTROL_FLOW":[TokenType.IF, TokenType.WHILE, TokenType.FOR, TokenType.SWITCH],
    "JUMP_STATEMENTS":[TokenType.RETURN, TokenType.GOTO, TokenType.BAILOUT, TokenType.BREAK, TokenType.CONTINUE]
}


# Error handling functions will be moved here
def contextful_unterminated_assignError(self):
    two_steps = 2
    alignment_extension = 2
    try:
        twice_prior = self.token_stream.peek_back(two_steps)
    except StopIteration:
        twice_prior = f"{self.token_stream.data[:((self.token_stream.cursor -1 ) if self.token_stream.cursor > 1 else self.token_stream.cursor)][-1].value}" if self.token_stream.cursor > 0 else "< Corrupted Internal State>"
    twice_prior = (twice_prior.value if not isinstance(twice_prior,str) else twice_prior) + " ="
    padding = "\n" + ((len(twice_prior) + alignment_extension) * ' ')
    found = self.token_stream.current() if self.token_stream.current() else "< EOF >" 
    expected = self.extensions["expected_next_tokens"](self)
    debug_message = f"^^^ <Rvalue aka {expected} needed/expected here but <{found}> provided >"
    error_type = "\nunterminated assignment\n"
    suggestion = (
        f"\nSuggestion: add a one of the expected types of tokens right to the right of the assignment sign aka '='" 
            if found == '< EOF >' else f" remove '{found.value}' and Put One Of The expected Types"
    )
    suggestion += f"\n{get_type_examples(expected)}"
    return f"{error_type}{twice_prior}{padding}{debug_message}{suggestion}"

def get_type_examples(types):
    sug = ""
    for type in types:
        match type:
            case TokenType.STRING_LITERAL:
                sug += "any valid ascii char enclosed inside double/single quote e.g('mark', 'my name is jullian', 'this is test string' etc...)"
            case TokenType.INTEGER:
                sug += "OR any base ten number (0,9) | No floats e.g(1,2,3,4,5,6,7,8,9,10 etc...)"
            case _:#will add more logic later/ this is testcase
                sug += ""
    return sug

def expected_next_tokens(self):
    curr = self.token_stream.current()
    if not curr:curr = self.token_stream.peek_back()
    match curr.type:
        case TokenType.IDENTIFIER:
            return [TokenType.EQUAL, TokenType.LPAREN]
        case TokenType.EQUAL:
            return [TokenType.IDENTIFIER, TokenType.STRING_LITERAL, TokenType.INTEGER]
        case _:
            return ["All Tokens Wont Be Valid After this CUrrent TYpe"]


Parser_extension_functions = {
    "errors":{
        "unterminated_assignment":contextful_unterminated_assignError
    },
    "Sentinel":{
        "expected_next_tokens":expected_next_tokens
    }
}