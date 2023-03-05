from ast_printer import AstPrinter
from expr import Assign, Binary, Expr, Grouping, Literal, Unary, Variable
from peu_token import PeuToken
from stmt import Block, Expression, Print, Stmt, Var
from token_type import TokenType


class PeuParser:
    def __init__(self, tokens: list[PeuToken]) -> None:
        self._tokens = tokens
        self._current = 0

    def parse(self) -> list[Stmt]:
        statements = []
        while not self._is_at_end():
            statements.append(self._declaration())

        return statements

    def _declaration(self):
        try:
            if self._match(TokenType.VAR):
                return self._var_declare()

            return self._statement()
        except ParseError:
            self._synchronize()
            return None

    def _var_declare(self):
        name = self._consume(TokenType.IDENTIFIER, "Expect variable name.")

        initializer = None
        if self._match(TokenType.EQUAL):
            initializer = self._expression()

        self._consume(
            TokenType.SEMICOLON, "Expect ';' after variable declaration."
        )
        return Var(name, initializer)

    def _statement(self) -> Stmt:
        if self._match(TokenType.PRINT):
            return self._print_statement()
        
        if self._match(TokenType.LEFT_BRACE):
            return Block(self._block())

        return self._expression_statement()
    
    def _block(self) -> list[Stmt]:
        statemements = []

        while not self._check(TokenType.RIGHT_BRACE) and not self._is_at_end():
            statemements.append(self._declaration())

        self._consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return statemements

    def _print_statement(self) -> Stmt:
        value = self._expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after value.")

        return Print(value)

    def _expression_statement(self) -> Stmt:
        value = self._expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after value.")

        return Expression(value)
    
    def _assignment(self) -> Expr:
        expr = self._equality()

        if (self._match(TokenType.EQUAL)):
            equals = self._previous()
            value = self._assignment()

            if isinstance(expr, Variable):
                name = expr.name
                return Assign(name, value)
        
            self._error(equals, "Invalid assignment target.")

        return expr

    def _expression(self) -> Expr:
        return self._assignment()

    def _equality(self) -> Expr:
        """equality       → comparison ( ( "!=" | "==" ) comparison )* ;"""
        expr = self._comparison()

        while self._match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self._previous()
            right = self._comparison()
            expr = Binary(expr, operator, right)

        return expr

    def _comparison(self) -> Expr:
        """comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;"""
        expr = self._term()

        while self._match(
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ):
            operator = self._previous()
            right = self._term()
            expr = Binary(expr, operator, right)

        return expr

    def _term(self) -> Expr:
        """term           → factor ( ( "-" | "+" ) factor )* ;"""
        expr = self._factor()

        while self._match(TokenType.MINUS, TokenType.PLUS):
            operator = self._previous()
            right = self._factor()
            expr = Binary(expr, operator, right)

        return expr

    def _factor(self) -> Expr:
        """factor         → unary ( ( "/" | "*" ) unary )* ;"""
        expr = self._unary()

        while self._match(TokenType.SLASH, TokenType.STAR):
            operator = self._previous()
            right = self._unary()
            expr = Binary(expr, operator, right)

        return expr

    def _unary(self) -> Expr:
        """unary          → ( "!" | "-" ) unary | primary ;"""

        if self._match(TokenType.BANG, TokenType.MINUS):
            operator = self._previous()
            right = self._unary()
            return Unary(operator, right)

        return self._primary()

    def _primary(self) -> Expr:
        """primary        → NUMBER | STRING | "true" | "false" | "null" | "(" expression ")" ;"""
        if self._match(TokenType.FALSE):
            return Literal(False)

        if self._match(TokenType.TRUE):
            return Literal(True)

        if self._match(TokenType.NULL):
            return Literal(None)

        if self._match(TokenType.NUMBER, TokenType.STRING):
            literalToken = self._previous()
            return Literal(literalToken.literal)

        if self._match(TokenType.IDENTIFIER):
            return Variable(self._previous())

        if self._match(TokenType.LEFT_PAREN):
            expr = self._expression()
            self._consume(
                TokenType.RIGHT_PAREN, "Expect ')' after expression."
            )
            return Grouping(expr)

        raise self._error(self._peek(), "Expect expression.")

    def _consume(self, type: TokenType, message: str) -> PeuToken:
        if self._check(type):
            return self._advance()

        raise self._error(self._peek(), message)

    def _error(self, token, message: str) -> None:
        # Peu.error(token, message)
        return ParseError()

    def _synchronize(self) -> None:
        self._advance()

        while not self._is_at_end():
            if self._previous().type == TokenType.SEMICOLON:
                return
            elif (
                self._peek().type == TokenType.CLASS
                or self._peek().type == TokenType.FUN
                or self._peek().type == TokenType.VAR
                or self._peek().type == TokenType.FOR
                or self._peek().type == TokenType.IF
                or self._peek().type == TokenType.WHILE
                or self._peek().type == TokenType.PRINT
                or self._peek().type == TokenType.RETURN
            ):
                return

            self._advance()

    def _match(self, *types: TokenType) -> bool:
        for type in types:
            if self._check(type):
                self._advance()
                return True

        return False

    def _check(self, type: TokenType) -> bool:
        if self._is_at_end():
            return False

        return self._peek().type == type

    def _advance(self) -> PeuToken:
        if not self._is_at_end():
            self._current += 1

        return self._previous()

    def _is_at_end(self) -> bool:
        return self._peek().type == TokenType.EOF

    def _peek(self) -> PeuToken:
        return self._tokens[self._current]

    def _previous(self) -> PeuToken:
        return self._tokens[self._current - 1]


class ParseError(RuntimeError):
    pass


def main():
    # - 123 * (45.67)
    tokens = [
        PeuToken(TokenType.MINUS, "-", None, 1),
        PeuToken(TokenType.NUMBER, "123", 123, 1),
        PeuToken(TokenType.STAR, "*", None, 1),
        PeuToken(TokenType.LEFT_PAREN, "(", None, 1),
        PeuToken(TokenType.NUMBER, "45.67", 45.67, 1),
        PeuToken(TokenType.RIGHT_PAREN, ")", None, 1),
        PeuToken(TokenType.EOF, "", None, 1),
    ]
    parser = PeuParser(tokens)
    printer = AstPrinter()
    expr = parser.parse()
    print(expr)
    print(printer.print(expr))


if __name__ == "__main__":
    main()
