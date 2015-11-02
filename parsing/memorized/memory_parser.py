import sys
import logging

from parsing.lexer.my_token import TYPE
from parsing.lexer.my_lexer import ListLexer


def debug_logging(func):
    def logged_func(*arg, **kwarg):
        logging.debug(func.__name__)
        result = func(*arg, **kwarg)
        return result
    return logged_func


class MemoryParser():

    def __init__(self, input):
        self.input = input
        self.markers = []
        self.lookahead = []
        self.listmemo = {}
        self.p = 0

    def __LT(self, i):
        self.sync(i)
        return self.lookahead[self.p + i - 1]

    def __LA(self, i):
        return self.__LT(i).type

    @debug_logging
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
        if self.p == len(self.lookahead) and not self.isSpeculating():
            self.p = 0
            self.lookahead = []
            self.clearMemo()
        self.sync(1)

    def clearMemo(self):
        self.listmemo = {}

    def isSpeculating(self):
        return len(self.markers) > 0

    def seek(self, index):
        self.p = index

    def mark(self):
        self.markers.append(self.p)
        return self.p

    def release(self):
        marker = self.markers.pop()
        self.seek(marker)

    def stat(self):
        logging.debug("stat")
        if self.speculate_stat_alt1():
            self.list()
            self.match(TYPE.EOF)
        elif self.speculate_stat_alt2():
            self.assign()
            self.match(TYPE.EOF)
        else:
            raise Exception("expecting a stat found %r" % self.__LT(1))

    def speculate_stat_alt1(self):
        logging.debug("speculate_stat_alt1")
        success = True
        self.mark()
        try:
            self.list()
            self.match(TYPE.EOF)
        except:
            success = False
        self.release()
        return success

    def speculate_stat_alt2(self):
        logging.debug("speculate_stat_alt2")
        success = True
        self.mark()
        try:
            self.assign()
            self.match(TYPE.EOF)
        except:
            success = False
        self.release()
        return success

    def assign(self):
        logging.debug("assgin")
        self.list()
        logging.debug("p: %d" % self.p)
        self.match(TYPE.EQUAL)
        self.list()

    @debug_logging
    def list(self):
        failed = False
        startTokenIndex = self.index()
        if (self.isSpeculating() and self.alreadyParsedRule(self.listmemo)):
            logging.debug("matched")
            return
        try:
            self._list()
        except Exception:
            failed = True
            raise
        finally:
            if self.isSpeculating():
                self.memoize(self.listmemo, startTokenIndex, failed)

    @debug_logging
    def alreadyParsedRule(self, memo):
        logging.debug(memo)
        memoI = memo.get(self.index(), None)
        if memoI is None:
            return False
        logging.debug("parsed list before at index " + str(self.index()) +
                      "; skip ahead to token index " + str(memoI) + ": " +
                      str(self.lookahead[memoI]))
        if memoI >= 0:
            self.seek(memoI)
            return True
        if memoI < 0:
            logging.debug("pared failed before")
            raise Exception("previous parsing failed")

    def memoize(self, memo, startTokenIndex, failed):
        stopTokenIndex = -1 if failed else self.index()
        memo[startTokenIndex] = stopTokenIndex

    @debug_logging
    def index(self):
        return self.p

    @debug_logging
    def _list(self):
        logging.debug(self.index())
        logging.debug("parse list rule at token index: " + str(self.index()))
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
    parser = MemoryParser(lexer)
    parser.stat()
