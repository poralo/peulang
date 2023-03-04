from peu_token import PeuToken

class Expr:
    def accept(self, visitor): pass

class Binary(Expr):
    def __init__(self, left: Expr, operator: PeuToken, right: Expr) -> None:
        super().__init__()

        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_binary(self)

class Grouping(Expr):
    def __init__(self, expression: Expr) -> None:
        super().__init__()

        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_grouping(self)

class Literal(Expr):
    def __init__(self, value: object) -> None:
        super().__init__()

        self.value = value

    def accept(self, visitor):
        return visitor.visit_literal(self)

class Unary(Expr):
    def __init__(self, operator: PeuToken, right: Expr) -> None:
        super().__init__()

        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_unary(self)

class Visitor:
    def visit_binary(self, expr: Binary): raise NotImplementedError

    def visit_grouping(self, expr: Grouping): raise NotImplementedError

    def visit_literal(self, expr: Literal): raise NotImplementedError

    def visit_unary(self, expr: Unary): raise NotImplementedError

