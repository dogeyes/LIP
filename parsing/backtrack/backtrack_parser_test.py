from parsing.backtrack.backtrack_parser import BacktrackParser
from parsing.lexer.my_lexer import ListLexer
import unittest


class TestTest(unittest.TestCase):

    def testBackTrackParser(self):
        s = '[a, b, [c, d], e] = [f, g, [h, i], j]'
        lexer = ListLexer(s)
        backtrack_parser = BacktrackParser(lexer)
        backtrack_parser.stat()


if __name__ == "__main__":
    unittest.main()
