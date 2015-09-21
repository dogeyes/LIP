import unittest
from parsing.multi.parser import Parser
from parsing.lexer.my_lexer import ListLexer


class MultiParserTest(unittest.TestCase):
    def testMultiParser(self):
        s = '[a, b, c=d, [e, f, g], h]'
        lexer = ListLexer(s)
        parser = Parser(lexer, 2)
        parser.list()
