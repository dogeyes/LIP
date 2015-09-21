import sys

from parsing.lexer.my_token import TYPE
from parsing.lexer.my_lexer import ListLexer


class Parser:
    def __init__(self, lexer, k):
        self.input = lexer
        self.lookaheads = list(None for _ in range(0, k))
        self.k = k
        self.p = 0
        for _ in range(0, k):
            self.consume()

    def consume(self):
        self.lookaheads[self.p] = self.input.nextToken()
        self.p = (self.p + 1) % self.k

    def __LT(self, i):
        return self.lookaheads[(self.p + self.k - 1) % self.k]

    def __LA(self, i):
        return self.__LT(i).type

    def match(self, t):
        if self.__LA(1) == t:
            self.consume()

    # grammar
    def list(self):
        self.match(TYPE.LBRACK)
        self.elements()
        self.match(TYPE.RBRACK)

    def elements(self):
        self.element()
        while self.__LA(1) == TYPE.COMMA:
            self.match(TYPE.COMMA)
            self.element()

    def element(self):
        if self.__LA(1) == TYPE.NAME and self.__LA(2) == TYPE.EQUAL:
            self.match(TYPE.NAME)
            self.match(TYPE.EQUAL)
            self.match(TYPE.NAME)
        elif self.__LA(1) == TYPE.NAME:
            self.match(TYPE.NAME)
        elif self.__LA(1) == TYPE.LBRACK:
            self.list()
        else:
            raise Exception("expecting name or list; found "
                            + str(self.__LT(1)))


if __name__ == "__main__":
    lexer = ListLexer(sys.argv[1])
    parser = Parser(lexer, 2)
    parser.list()
