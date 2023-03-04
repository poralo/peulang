from token_type import TokenType

class PeuToken:
    def __init__(
        self, 
        type: TokenType, 
        lexeme: str, 
        literal: object, 
        line: int
    ) -> None:
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __repr__(self) -> str:
        return f"{self.type} {self.lexeme} {self.literal}"