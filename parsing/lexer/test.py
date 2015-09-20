from enum import Enum
import sys


class Token(object):
    def __init__(self, _content, _type):
        self.content = _content
        self.type = _type

    def __repr__(self):
        return "<'%s', %s>" % (self.content, self.type)

    def __eq__(self, t):
        return self.content == t.content and self.type == t.type


class TYPE(Enum):
    LBRACK = 0
    RBRACK = 1
    COMMA = 2
    NAME = 3
    EOF = 4


class ListLexer(object):
    def __init__(self, _content):
        self.content = _content
        self.index = 0

    def nextToken(self):
        while(self.index < len(self.content)):
            c = self.content[self.index]
            self.index += 1
            if c is ',':
                return Token(',', TYPE.COMMA)
            elif c is '[':
                return Token('[', TYPE.LBRACK)
            elif c is ']':
                return Token(']', TYPE.RBRACK)
            elif c in [' ', '\t', '\n']:
                continue
            else:
                return Token(c, TYPE.NAME)
        return Token('<EOF>', TYPE.EOF)


if __name__ == "__main__":
    lexer = ListLexer(sys.argv[1])
    t = lexer.nextToken()
    while not t.type == TYPE.EOF:
        print(t)
        t = lexer.nextToken()
    print(t)
