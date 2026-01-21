from util.iohelpers import panic
from util.facilitators import StreamIterator
from type_decl.lexer_types import RESERVED, CTOT_MAP, TokenType, Token





class Lexer:
    def __init__(self,data):
        self.data = data.lstrip().rstrip()
        self.stream = StreamIterator(self.data,label="Raw String Stream")
        self.tmp = None 
        self.tokens_output = []
        self.neglect = [" ","\t","\n", "\r"]
        self.quotes = [TokenType.DOUBLE_QUOTE, TokenType.SINGLE_QUOTE]
    def start_lexer_loop(self):
        while self.stream.has_next():
            self.skip_tokens()
            if self.get_pair_charop():
                if self.tmp.type == TokenType.BULK_COMMENT_TAG_LEFT:
                    self.tmp = Token(TokenType.COMMENT,self.pair_lookup_collect_until(TokenType.BULK_COMMENT_TAG_RIGHT.value))
                else:
                    self.stream.next()
                    self.stream.next()
                self.tokens_output.append(self.tmp)
                continue
            else:
                if self.stream.current() in CTOT_MAP:
                    token = Token(CTOT_MAP.get(self.stream.current(),TokenType.ILLEGAL_SYMBOL),self.stream.current())
                    if token.type == TokenType.TAG:
                        token = self.collect_until("\n",type=TokenType.COMMENT)
                    elif token.type in self.quotes:
                        token = self.collect_string_literal_after_quote(token)
                    self.tokens_output.append(token)
                    self.stream.next()
                else:
                    token = self.collect_until(type=TokenType.IDENTIFIER)
                    if token:
                        if token.value in RESERVED:
                            keyword_token_type = CTOT_MAP.get(token.value, TokenType.KEYWORD)
                            token = self.convert_token_type(token, keyword_token_type)
                        if token.type != TokenType.ILLEGAL_SYMBOL:self.tokens_output.append(token)
                        else:self.raise_error(f"Illegal symbol : {self.stream.return_formatted_state()}")
                    else:
                        self.raise_error(f"Illegal symbol : {self.stream.return_formatted_state()}")
    def pair_lookup_collect_until(self,delim):
        n = 0
        value = ""
        while self.stream.has_next():
            if self.stream.peek(n) == delim[0] and self.stream.peek(n+1) == delim[1]:
                n += 1
                break
            n+=1
        value = "".join([self.stream.peek(i) for i in range(n+1)])
        for i in range(n+1):
            self.stream.next()
        return value
    def convert_token_type(self,tok:Token,type:TokenType):
        return Token(type,tok.value)
    def raise_error(self,message:str):
        panic(message)
    def collect_until(self, delim: str = None, type: TokenType = TokenType.IDENTIFIER):
            ident = ""
            # Loop while the CURRENT character is valid
            while self.stream.has_next():
                curr = self.stream.current()
                cond = (curr != delim) if delim else self.isalphanum(curr)
                
                if not cond:
                    break
                    
                ident += curr
                self.stream.next() # Move to the next char immediately
                
            return Token(type, ident) if ident else None
    def isalphanum(self,char:str):
        return char.isdigit() or char.isalpha() or char == "_"
    def skip_tokens(self):
        while self.stream.has_next() and self.stream.current() in self.neglect:
            self.stream.next()
    def collect_string_literal_after_quote(self,quote:Token):
        n = 1
        value = ""
        peeked_val = ""
        while self.stream.has_next():
            try:
                peeked_val = self.stream.peek(n)
            except StopIteration:
                break
            if peeked_val == "\n" or peeked_val == quote.value:
                break
            value += self.stream.peek(n)
            n+=1
        if peeked_val != quote.value:
            raise Exception("Unterminated string literal")
        else:
            for i in range(n):
                self.stream.next()
            return Token(TokenType.STRING_LITERAL,value)
    def get_pair_charop(self):
        try:
            next = self.stream.peek()
        except StopIteration:
            return False
        pair_op = f"{self.stream.current()}{next}"
        if  pair_op in CTOT_MAP:
            self.tmp = Token(CTOT_MAP.get(pair_op,TokenType.ILLEGAL_SYMBOL),pair_op)
            return True
        return False
    def clean_single_token(self,token,tokens:list,iter:StreamIterator):
        fuck = True
        try:
            if token.value.isdigit():
                tokens.append(Token(TokenType.INTEGER,int(token.value)));fuck = False
        except AttributeError:
            pass
        if fuck:
            tokens.append(token)
        iter.next()
    def tokenize(self):
        self.start_lexer_loop()
        tok_iter = StreamIterator(self.tokens_output,label="Token List")
        new_list = []
        quotes = [TokenType.DOUBLE_QUOTE, TokenType.SINGLE_QUOTE]
        while tok_iter.has_next():
            curr = tok_iter.current()
            if curr.type in quotes:
                try:
                    twice_ahead = tok_iter.peek(2)
                    ident = tok_iter.peek()
                except StopIteration:
                    self.clean_single_token(curr,new_list,tok_iter)
                    continue
                if ident.type == TokenType.IDENTIFIER and twice_ahead.type in quotes and tok_iter.current().type == twice_ahead.type:
                    new_list.append(Token(TokenType.STRING_LITERAL,ident.value))
                    for i in range(3):
                        tok_iter.next()
                if ident.type in quotes and ident.type == curr.type:
                    new_list.append(Token(TokenType.STRING_LITERAL,""))
                    for i in range(2):
                        tok_iter.next()
                else:
                    self.clean_single_token(curr,new_list,tok_iter)
            else:
                self.clean_single_token(curr,new_list,tok_iter)
        self.cleaned_tokens = new_list
        return StreamIterator(self.cleaned_tokens,label="Parsing Ready Post-Lexing Tokens"),self.cleaned_tokens