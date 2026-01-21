class AssignmentNode:
    def __init__(self, lvalue, lvalue_type, rvalue, rvalue_type):
        self.lhs = lvalue
        self.rhs = rvalue
        self.enforce_type(lvalue_type, rvalue_type)
    def enforce_type(self, lhs_type, rhs_type):
        if lhs_type != rhs_type and lhs_type != TokenType.IDENT:#IDENT is the required lvalue that will hold the mem address in the heap for the assigned rhs
            raise TypeError(
                f"Can't assign value from type '{rhs_type}'"
                f"to an identifier of type {lhs_type}"
            )
        else:pass
    def process(self):
        pass
    def __repr__(self):
        return f"AssignmentNode(lhs='{repr(self.lhs)}',rhs={repr(self.rhs)})"



class StreamIterator:
    def __init__(self, data: str, label: str = "In Memory Str Object"):
        self.data = data
        self.label = label
        self.cursor = 0
        self.line_no = 1
        self.column_no = 1

    def peek(self, step=1):
        target = self.cursor + step
        if 0 <= target < len(self.data):
            return self.data[target]
        raise StopIteration("Peek out of bounds")

    def next(self):
        if not self.has_next():
            raise StopIteration
        
        char = self.data[self.cursor]
        self.cursor += 1

        if char == "\n":
            self.line_no += 1
            self.column_no = 1
        else:
            self.column_no += 1
        return char

    def undo(self):
        if self.cursor <= 0:
            raise ValueError("Start of stream")
        
        self.cursor -= 1
        char = self.data[self.cursor]

        if char == "\n":
            self.line_no -= 1
            prev_nl = self.data.rfind('\n', 0, self.cursor)
            self.column_no = self.cursor - prev_nl
        else:
            self.column_no -= 1
        return char

    def has_next(self):
        return self.cursor < len(self.data)

    def current(self):
        return self.data[self.cursor] if self.has_next() else None

    def reset(self):
        self.__init__(self.data, self.label)
    def peek_back(self,n=1):
        if n<1:
            raise ValueError("Dude are you dumb? what the hell does 'Negative History Resolution' Even Mean ?")
        if self.cursor >= n:
            return self.data[self.cursor - n]
        raise StopIteration("Damn! Seems-like I cant ' peek_back ' {} steps : the best i can do rn is ' peek_back ' {} steps".format(n,self.cursor))

    def return_formatted_state(self):
        char = self.current() or "EOF"
        return f'"{repr(char)}" at line {self.line_no} col {self.column_no} in "{self.label}"'