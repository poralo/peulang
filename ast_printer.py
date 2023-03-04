from expr import Binary, Expr, Grouping, Literal, Unary, Visitor
from peu_token import PeuToken
from token_type import TokenType


class AstPrinter(Visitor):
    def print(self, expr: Expr):
        return expr.accept(self)
    
    def visit_binary(self, expr: Binary):
        return self._parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping(self, expr: Grouping):
        return self._parenthesize("group", expr.expression)

    def visit_literal(self, expr: Literal):
        if (expr.value == None):
            return "null"
        
        return str(expr.value)

    def visit_unary(self, expr: Unary):
        return self._parenthesize(expr.operator.lexeme, expr.right)
    
    def _parenthesize(self, name, *exprs):
        inner_expr = " ".join([expr.accept(self) for expr in exprs])
        return f"({name} {inner_expr})"


def main():
    expression = Binary(
        Unary(PeuToken(TokenType.MINUS, "-", None, 1), Literal(123)),
        PeuToken(TokenType.STAR, "*", None, 1),
        Grouping(Literal(45.67))
    )
    printer = AstPrinter()
    print(printer.print(expression))

if __name__ == "__main__":
    main()