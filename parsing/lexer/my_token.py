from enum import Enum


class TYPE(Enum):
    LBRACK = 0
    RBRACK = 1
    COMMA = 2
    NAME = 3
    EOF = 4


class Token(object):
    def __init__(self, _content, _type):
        self.content = _content
        self.type = _type

    def __repr__(self):
        return "<'%s', %s>" % (self.content, self.type)

    def __eq__(self, t):
        return self.content == t.content and self.type == t.type

