from parsing.memorized.memory_parser import MemoryParser
from parsing.lexer.my_lexer import ListLexer
import unittest
import logging
logging.basicConfig(level=logging.ERROR)


class TestTest(unittest.TestCase):

    def testBackTrackParser(self):
        s = '[a, b, [c, d], e] = [f, g, [h, i], j]'
        lexer = ListLexer(s)
        memory_parser = MemoryParser(lexer)
        memory_parser.stat()


if __name__ == "__main__":
    unittest.main()
