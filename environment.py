from error import PeuRuntimeError
from peu_token import PeuToken


class Environment:
    def __init__(self) -> None:
        self._values = dict()

    def define(self, name: str, value: object) -> None:
        self._values[name] = value

    def get(self, name: PeuToken) -> object:
        value = self._values.get(name.lexeme)

        if (value is None):
            raise PeuRuntimeError(name, f"Undefined variable '{name.lexeme}'.")
        
        return value
    
    def assign(self, name: PeuToken, value: object) -> None:
        current_value = self._values.get(name.lexeme)

        if (current_value is None):
            raise PeuRuntimeError(name, f"Undefined variable '{name.lexeme}'.")
        
        self._values[name.lexeme] = value