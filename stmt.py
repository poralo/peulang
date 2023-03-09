from expr import Expr
from peu_token import PeuToken

class Stmt:
    def accept(self, visitor): pass

class Block(Stmt):
    def __init__(self, statements: list[Stmt]) -> None:
        super().__init__()

        self.statements = statements

    def accept(self, visitor):
        return visitor.visit_block(self)

    def __repr__(self) -> str:
        return f"Block({self.statements})"

class Expression(Stmt):
    def __init__(self, expression: Expr) -> None:
        super().__init__()

        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_expression(self)

    def __repr__(self) -> str:
        return f"Expression({self.expression})"

class If(Stmt):
    def __init__(self, condition: Expr, then_branch: Stmt, else_branch: Stmt) -> None:
        super().__init__()

        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def accept(self, visitor):
        return visitor.visit_if(self)

    def __repr__(self) -> str:
        return f"If({self.condition}, {self.then_branch}, {self.else_branch})"

class Print(Stmt):
    def __init__(self, expression: Expr) -> None:
        super().__init__()

        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_print(self)

    def __repr__(self) -> str:
        return f"Print({self.expression})"

class Var(Stmt):
    def __init__(self, name: PeuToken, initializer: Expr) -> None:
        super().__init__()

        self.name = name
        self.initializer = initializer

    def accept(self, visitor):
        return visitor.visit_var(self)

    def __repr__(self) -> str:
        return f"Var({self.name}, {self.initializer})"

class Visitor:
    def visit_block(self, stmt: Block): raise NotImplementedError

    def visit_expression(self, stmt: Expression): raise NotImplementedError

    def visit_if(self, stmt: If): raise NotImplementedError

    def visit_print(self, stmt: Print): raise NotImplementedError

    def visit_var(self, stmt: Var): raise NotImplementedError

