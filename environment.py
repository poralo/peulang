from error import PeuRuntimeError
from peu_token import PeuToken


class Environment:
    def __init__(self, enclosing = None) -> None:
        self._values = dict()
        self.enclosing = enclosing

    def define(self, name: str, value: object) -> None:
        self._values[name] = value

    def get(self, name: PeuToken) -> object:
        value = self._values.get(name.lexeme)

        if value is None:
            if self.enclosing is None:
                raise PeuRuntimeError(name, f"Undefined variable '{name.lexeme}'.")
            
            return self.enclosing.get(name)
        
        return value
    
    def assign(self, name: PeuToken, value: object) -> None:
        current_value = self._values.get(name.lexeme)

        if (current_value is None):
            if self.enclosing is None:
                raise PeuRuntimeError(name, f"Undefined variable '{name.lexeme}'.")
            
            self.enclosing.assign(name, value)
            return
            
        self._values[name.lexeme] = value