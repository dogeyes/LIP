import sys

from parsing.lexer.my_token import TYPE
from parsing.lexer.my_lexer import ListLexer


class BacktrackParser():

    def __init__(self, input):
        self.input = input
        self.markers = []
        self.lookahead = []
        self.p = 0
        self.isSpeculating = False

    def __LT(self, i):
        self.sync(i)
        return self.lookahead[self.p + i - 1]

    def __LA(self, i):
        return self.__LT(i).type

    def match(self, x):
        if self.__LA(1) == x:
            self.consume()
        else:
            raise Exception("expecting " +
                            x + " found " + self.__LT(1))

    def sync(self, i):
        """Expend the token buff,
        make sure we have i tokens from current position p"""
        if len(self.lookahead) > self.p + i - 1:
            return
        n = self.p + i - len(self.lookahead)
        self.fill(n)

    def fill(self, n):
        for i in range(0, n):
            self.lookahead.append(self.input.nextToken())

    def consume(self):
        self.p += 1
        if self.p == len(self.lookahead) and not self.isSpeculating:
            self.p = 0
            self.lookahead = []

    def seek(self, index):
        self.p = index

    def mark(self):
        self.markers.append(self.p)
        return self.p

    def release(self):
        marker = self.markers.pop()
        self.seek(marker)

    def stat(self):
        if self.speculate_stat_alt1():
            self.list()
            self.match(TYPE.EOF)
        elif self.speculate_stat_alt2():
            self.assign()
            self.match(TYPE.EOF)
        else:
            raise Exception("expecting a stat found %r" % self.__LT(1))

    def speculate_stat_alt1(self):
        success = True
        self.isSpeculating = True
        self.mark()
        try:
            self.list()
            self.match(TYPE.EOF)
        except:
            success = False
        self.release()
        self.isSpeculating = False
        return success

    def speculate_stat_alt2(self):
        success = True
        self.isSpeculating = True
        self.mark()
        try:
            self.assign()
            self.match(TYPE.EOF)
        except:
            success = False
        self.release()
        self.isSpeculating = False
        return success

    def assign(self):
        self.list()
        self.match(TYPE.EQUAL)
        self.list()

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
            self.match(TYPE.EQUAK)
            self.match(TYPE.NAME)
        elif self.__LA(1) == TYPE.NAME:
            self.match(TYPE.NAME)
        elif self.__LA(1) == TYPE.LBRACK:
            self.list()
        else:
            raise Exception("expecting name or list; found %s" %
                            str(self.__LT(1)))


if __name__ == "__main__":
    lexer = ListLexer(sys.argv[1])
    parser = BacktrackParser(lexer)
    parser.stat()
