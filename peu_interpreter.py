from environment import Environment
from error import PeuRuntimeError
from expr import Assign, Binary, Expr, Grouping, Literal, Unary, Variable, Visitor as ExprVisitor
from peu_token import PeuToken
from stmt import Block, Expression, Print, Stmt, Var, Visitor as StmtVisitor
from token_type import TokenType


class Interpreter(ExprVisitor, StmtVisitor):
    def __init__(self) -> None:
        super().__init__()

        self._environment = Environment()

    def interpret(self, statements: list[Stmt]) -> None:
        try:
            for statement in statements:
                self._execute(statement)
        except PeuRuntimeError:
            pass

    def _execute(self, statement: Stmt):
        statement.accept(self)

    def _execute_block(self, statements: list[Stmt], environment: Environment) -> None:
        previous = self._environment

        try:
            self._environment = environment

            for statement in statements:
                self._execute(statement)
        finally:
            self._environment = previous

    def _stringify(self, value: object) -> str:
        if value is None:
            return "null"

        if isinstance(value, bool):
            if bool(value):
                return "true"
            return "false"

        return str(value)
    
    def visit_block(self, stmt: Block) -> None:
        self._execute_block(stmt.statements, Environment(self._environment))

    def visit_expression(self, stmt: Expression):
        self._evaluate(stmt.expression)

    def visit_print(self, stmt: Print):
        value = self._evaluate(stmt.expression)
        print(self._stringify(value))

    def visit_var(self, stmt: Var):
        value = None
        if (stmt.initializer != None):
            value = self._evaluate(stmt.initializer)

        self._environment.define(stmt.name.lexeme, value)
        return None
    
    def visit_assign(self, expr: Assign) -> object:
        value = self._evaluate(expr.value)
        self._environment.assign(expr.name, value)

        return value

    def visit_binary(self, expr: Binary) -> object:
        left = self._evaluate(expr.left)
        right = self._evaluate(expr.right)

        if expr.operator.type == TokenType.GREATER:
            self._check_number_operands(expr.operator, left, right)
            return float(left) > float(right)
        elif expr.operator.type == TokenType.GREATER_EQUAL:
            self._check_number_operands(expr.operator, left, right)
            return float(left) >= float(right)
        elif expr.operator.type == TokenType.LESS:
            self._check_number_operands(expr.operator, left, right)
            return float(left) < float(right)
        elif expr.operator.type == TokenType.LESS_EQUAL:
            self._check_number_operands(expr.operator, left, right)
            return float(left) <= float(right)
        elif expr.operator.type == TokenType.EQUAL_EQUAL:
            self._check_number_operands(expr.operator, left, right)
            return self._is_equal(left, right)
        elif expr.operator.type == TokenType.BANG_EQUAL:
            return not self._is_equal(left, right)
        elif expr.operator.type == TokenType.MINUS:
            self._check_number_operands(expr.operator, left, right)
            return float(left) - float(right)
        elif expr.operator.type == TokenType.PLUS:
            if isinstance(left, float) and isinstance(right, float):
                return float(left) + float(right)
            elif isinstance(left, str) and isinstance(right, str):
                return str(left) + str(right)

            raise PeuRuntimeError(
                expr.operator, "Operands must be two numbers or two strings."
            )
        elif expr.operator.type == TokenType.SLASH:
            self._check_number_operands(expr.operator, left, right)
            return float(left) / float(right)
        elif expr.operator.type == TokenType.STAR:
            self._check_number_operands(expr.operator, left, right)
            return float(left) * float(right)

        return None

    def visit_grouping(self, expr: Grouping) -> object:
        return self._evaluate(expr.expression)

    def visit_literal(self, expr: Literal) -> object:
        return expr.value

    def visit_unary(self, expr: Unary) -> object:
        right = self._evaluate(expr.right)

        if expr.operator.type == TokenType.MINUS:
            self._check_number_operand(expr.operator, right)
            return -float(right)
        elif expr.operator.type == TokenType.BANG:
            return not self._is_truthy(right)

        return None
    
    def visit_variable(self, expr: Variable) -> object:
        return self._environment.get(expr.name)

    def _evaluate(self, expr: Expr) -> object:
        return expr.accept(self)

    def _is_truthy(self, value: object) -> bool:
        if value is None:
            return False
        elif isinstance(value, bool):
            return bool(value)
        elif isinstance(value, float):
            return float(value) == 0
        elif isinstance(value, str):
            return str(value) == ""

        return True

    def _is_equal(self, left: object, right: object) -> bool:
        return left == right

    def _check_number_operand(
        self, operator: PeuToken, operand: object
    ) -> bool:
        if isinstance(operand, float):
            return
        raise PeuRuntimeError(operator, "Operand must be a number.")

    def _check_number_operands(
        self, operator: PeuToken, left: object, right: object
    ) -> bool:
        if isinstance(left, float) and isinstance(right, float):
            return
        raise PeuRuntimeError(operator, "Operands must be a number.")