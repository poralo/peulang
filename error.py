from peu_token import PeuToken


class PeuRuntimeError(RuntimeError):
    def __init__(self, token: PeuToken, message: str, *args: object) -> None:
        super().__init__(*args)

        self.token = token
        self.message = message
