from peu_token import PeuToken

class Expr:
    def accept(self, visitor): pass

class Assign(Expr):
    def __init__(self, name: PeuToken, value: Expr) -> None:
        super().__init__()

        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visit_assign(self)

    def __repr__(self) -> str:
        return f"Assign({self.name}, {self.value})"

class Binary(Expr):
    def __init__(self, left: Expr, operator: PeuToken, right: Expr) -> None:
        super().__init__()

        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_binary(self)

    def __repr__(self) -> str:
        return f"Binary({self.left}, {self.operator}, {self.right})"

class Grouping(Expr):
    def __init__(self, expression: Expr) -> None:
        super().__init__()

        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_grouping(self)

    def __repr__(self) -> str:
        return f"Grouping({self.expression})"

class Literal(Expr):
    def __init__(self, value: object) -> None:
        super().__init__()

        self.value = value

    def accept(self, visitor):
        return visitor.visit_literal(self)

    def __repr__(self) -> str:
        return f"Literal({self.value})"

class Unary(Expr):
    def __init__(self, operator: PeuToken, right: Expr) -> None:
        super().__init__()

        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_unary(self)

    def __repr__(self) -> str:
        return f"Unary({self.operator}, {self.right})"

class Variable(Expr):
    def __init__(self, name: PeuToken) -> None:
        super().__init__()

        self.name = name

    def accept(self, visitor):
        return visitor.visit_variable(self)

    def __repr__(self) -> str:
        return f"Variable({self.name})"

class Visitor:
    def visit_assign(self, expr: Assign): raise NotImplementedError

    def visit_binary(self, expr: Binary): raise NotImplementedError

    def visit_grouping(self, expr: Grouping): raise NotImplementedError

    def visit_literal(self, expr: Literal): raise NotImplementedError

    def visit_unary(self, expr: Unary): raise NotImplementedError

    def visit_variable(self, expr: Variable): raise NotImplementedError

