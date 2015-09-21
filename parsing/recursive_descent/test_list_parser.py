"""Test for list parser."""
from parsing.lexer.my_lexer import ListLexer
from parsing.recursive_descent.list_parser import ListParser
import unittest


class TestListParser(unittest.TestCase):
    def testListParser(self):
        s = "[a, b, [c, dg], e]"
        lexer = ListLexer(s)
        paser = ListParser(lexer)
        paser.list()


if __name__ == "__main__":
    unittest.main()
