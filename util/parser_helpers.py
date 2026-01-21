from type_decl.lexer_types import TokenType


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

def get_type_examples(types:[TokenType]):
    sug = ""
    for type in types:
        match type:
            case TokenType.STRING_LITERAL:
                sug += "any valid ascii char enclosed inside double/single quote e.g('mark', 'my name is jullian', 'this is test string' etc...)"
            case TokenType.INTEGER_LITERAL:
                sug += "OR any base ten number (0,9) | No floats e.g(1,2,3,4,5,6,7,8,9,10 etc...)"
            case _:#will add more logic later/ this is testcase
                sug += ""
    return sug
def expected_next_tokens(self):
    curr = self.token_stream.current()
    if not curr:curr = self.token_stream.peek_back()
    match curr.type:
        case TokenType.IDENT:
            return [TokenType.EQUAL, "TokenType.LPAREN"]
        case TokenType.EQUAL:
            return [TokenType.IDENT, TokenType.STRING_LITERAL, TokenType.INTEGER_LITERAL]
        case _:
            return ["All Tokens Wont Be Valid After this CUrrent TYpe"]


