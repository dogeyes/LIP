"""Test for test.py"""
import test
import unittest


class TestTest(unittest.TestCase):

    def testListLexer(self):
        s = '[a, b]'
        lexer = test.ListLexer(s)
        t = lexer.nextToken()
        self.assertEqual(test.Token('[', test.TYPE.LBRACK), t)
        t = lexer.nextToken()
        self.assertEqual(test.Token('a', test.TYPE.NAME), t)
        t = lexer.nextToken()
        self.assertEqual(test.Token(',', test.TYPE.COMMA), t)
        t = lexer.nextToken()
        self.assertEqual(test.Token('b', test.TYPE.NAME), t)
        t = lexer.nextToken()
        self.assertEqual(test.Token(']', test.TYPE.RBRACK), t)
        t = lexer.nextToken()
        self.assertEqual(test.Token('<EOF>', test.TYPE.EOF), t)

if __name__ == "__main__":
    unittest.main()
