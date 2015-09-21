import sys
from parsing.lexer.my_token import Token
from parsing.lexer.my_token import TYPE


class Lexer:
    def nextToken(self):
        pass


class ListLexer(Lexer):

    def __init__(self, _content):
        self.content = _content
        self.index = 0
        self.c = self.content[self.index]

    def __consume(self):
        self.index += 1
        if self.index == len(self.content):
            self.c = None
        else:
            self.c = self.content[self.index]

    def __isLetter(self):
        return (('a' <= self.c and self.c <= 'z')
                or ('A' <= self.c and self.c <= 'Z'))

    def __WS(self):
        while(self.c in [' ', '\t', '\n', '\r']):
            self.__consume()

    def __NAME(self):
        name = ""
        while(self.__isLetter()):
            name += self.c
            self.__consume()
        return Token(name, TYPE.NAME)

    def nextToken(self):
        while(self.c is not None):
            if self.c is ',':
                self.__consume()
                return Token(',', TYPE.COMMA)
            elif self.c is '[':
                self.__consume()
                return Token('[', TYPE.LBRACK)
            elif self.c is ']':
                self.__consume()
                return Token(']', TYPE.RBRACK)
            elif self.c is '=':
                return Token('=', TYPE.EQUAL)
            elif self.c in [' ', '\t', '\n', '\r']:
                self.__WS()
                continue
            else:
                if self.__isLetter():
                    return self.__NAME()
        return Token('<EOF>', TYPE.EOF)


if __name__ == "__main__":
    lexer = ListLexer(sys.argv[1])
    t = lexer.nextToken()
    while not t.type == TYPE.EOF:
        print(t)
        t = lexer.nextToken()
    print(t)
