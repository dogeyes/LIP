import sys
from parsing.lexer.my_token import TYPE
from parsing.lexer.my_lexer import ListLexer


class Parser:
    pass


class ListParser(Parser):
    def __init__(self, _input):
        self.input = _input
        self.lookahead = self.input.nextToken()

    def consume(self):
        self.lookahead = self.input.nextToken()

    def match(self, t):
        if self.lookahead.type == t:
            self.consume()
        else:
            raise Exception("expecting " + str(t) +
                            "; found " + str(self.lookahead))

    # grammer
    def list(self):
        self.match(TYPE.LBRACK)
        self.elements()
        self.match(TYPE.RBRACK)

    def elements(self):
        self.element()
        while self.lookahead.type == TYPE.COMMA:
            self.match(TYPE.COMMA)
            self.element()

    def element(self):
        if self.lookahead.type == TYPE.NAME:
            return self.match(TYPE.NAME)
        elif self.lookahead.type == TYPE.LBRACK:
            return self.list()
        else:
            raise Exception("expecting name or list: found " + self.lookahead)


if __name__ == "__main__":
    lexer = ListLexer(sys.argv[1])
    parser = ListParser(lexer)
    parser.list()
