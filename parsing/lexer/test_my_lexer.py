"""Test for test.py"""
from parsing.lexer.my_token import Token
from parsing.lexer.my_token import TYPE
import unittest
from parsing.lexer.my_lexer import ListLexer


class TestTest(unittest.TestCase):

    def testListLexer(self):
        s = '[a, b]'
        lexer = ListLexer(s)
        t = lexer.nextToken()
        self.assertEqual(Token('[', TYPE.LBRACK), t)
        t = lexer.nextToken()
        self.assertEqual(Token('a', TYPE.NAME), t)
        t = lexer.nextToken()
        self.assertEqual(Token(',', TYPE.COMMA), t)
        t = lexer.nextToken()
        self.assertEqual(Token('b', TYPE.NAME), t)
        t = lexer.nextToken()
        self.assertEqual(Token(']', TYPE.RBRACK), t)
        t = lexer.nextToken()
        self.assertEqual(Token('<EOF>', TYPE.EOF), t)


if __name__ == "__main__":
    unittest.main()
