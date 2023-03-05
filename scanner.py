#from peu import Peu
from token_type import TokenType
from peu_token import PeuToken

class Scanner:
    keywords = {
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "for": TokenType.FOR,
        "fun": TokenType.FUN,
        "if": TokenType.IF,
        "null": TokenType.NULL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "while": TokenType.WHILE,
    }

    def __init__(self, source: str) -> None:
        self._source = source
        self._tokens = []

        self._start = 0
        self._current = 0
        self._line = 1
    
    def scan_tokens(self):
        while not self._isAtEnd():
            self._start = self._current
            self._scan_token()

        self._tokens.append(PeuToken(TokenType.EOF, "", None, self._line))
        return self._tokens

    def _isAtEnd(self) -> bool:
        return self._current >= len(self._source)

    def _scan_token(self):
        ch = self._next()
        if ch == '(':
            self._add_token(TokenType.LEFT_PAREN)
        elif ch == ')':
            self._add_token(TokenType.RIGHT_PAREN)
        elif ch == '{':
            self._add_token(TokenType.LEFT_BRACE)
        elif ch == '}':
            self._add_token(TokenType.RIGHT_BRACE)
        elif ch == ',':
            self._add_token(TokenType.COMMA)
        elif ch == '.':
            self._add_token(TokenType.DOT)
        elif ch == '-':
            self._add_token(TokenType.MINUS)
        elif ch == '+':
            self._add_token(TokenType.PLUS)
        elif ch == ';':
            self._add_token(TokenType.SEMICOLON)
        elif ch == '*':
            self._add_token(TokenType.STAR)
        elif ch == '!':
            if self._match("="):
                self._add_token(TokenType.BANG_EQUAL)
            else:
                self._add_token(TokenType.BANG)
        elif ch == '=':
            if self._match("="):
                self._add_token(TokenType.EQUAL_EQUAL)
            else:
                self._add_token(TokenType.EQUAL)
        elif ch == '<':
            if self._match("="):
                self._add_token(TokenType.LESS_EQUAL)
            else:
                self._add_token(TokenType.LESS)
        elif ch == '>':
            if self._match("="):
                self._add_token(TokenType.GREATER_EQUAL)
            else:
                self._add_token(TokenType.GREATER)
        elif ch == '/':
            if self._match("/"):
                while self.peek() != '\n' and not self._isAtEnd():
                    self._next()
            else:
                self._add_token(TokenType.SLASH)
        elif ch == ' ' or ch == '\r' or ch == '\t':
            pass
        elif ch == '\n':
            self._line += 1
        elif ch == "\"":
            self.string()
        else:
            if ch.isdigit():
                self.number()
            elif ch.isalpha():
                self.identifier()
            else:
                #Peu.error(self._line, "Unexpected character.")
                pass

    def _next(self):
        ch = self._source[self._current]
        self._current += 1
        return ch
    
    def _match(self, expected: str):
        if self._isAtEnd():
            return False
        elif self._source[self._current] != expected:
            return False
        
        self._current += 1
        return True

    def _peek(self) -> str:
        if (self._isAtEnd()):
            return '\0'

        return self._source[self._current]

    def _peek_next(self) -> str:
        if self._current + 1 >= len(self._source):
            return '\0'

        return self._source[self._current + 1]

    def _add_token(self, type: TokenType):
        self._add_token_literal(type, None)

    def _add_token_literal(self, type: TokenType, literal: object):
        text = self._source[self._start:self._current]
        self._tokens.append(PeuToken(type, text, literal, self._line))

    def string(self):
        while self._peek() != '"' and not self._isAtEnd():
            if self._peek() == "\n":
                self._line += 1
            self._next()

        if self._isAtEnd():
            #Peu.error(self._line, "Unterminated string.")
            return

        # The closing ".
        self._next()

        # Trim the surrounding quotes.
        value = self._source[self._start + 1: self._current - 1]
        self._add_token_literal(TokenType.STRING, value)

    def number(self):
        while self._peek().isdigit():
            self._next()

        # Look for a fractional part.
        if (self._peek() == '.' and self._peek_next().isdigit()):
            # Consume the "."
            self._next()

            while self._peek().isdigit():
                self._next()

        self._add_token_literal(
            TokenType.NUMBER, 
            float(self._source[self._start:self._current])
        )
    
    def identifier(self):
        while self._peek().isalnum():
            self._next()

        text = self._source[self._start:self._current]
        type = Scanner.keywords.get(text)
        if type is None:
            type = TokenType.IDENTIFIER
        self._add_token(type)