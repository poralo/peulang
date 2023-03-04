import sys
from peu_interpreter import Interpreter
from peu_parser import PeuParser
from peu_token import PeuToken
from scanner import Scanner
from ast_printer import AstPrinter
from token_type import TokenType

class Peu:
    had_error = False
    had_runtime_error = False
    interpreter = Interpreter()
        
    def run(self, source: str) -> None:
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        parser = PeuParser(tokens)
        expr = parser.parse()

        # Stop si il y a eu une erreur de syntaxe
        if self.had_error or expr is None:
            return

        # print(AstPrinter().print(expr))
        Peu.interpreter.interpret(expr)

    def run_file(self, path: str) -> None:
        with open(path) as file:
            self.run(file.read())

        if Peu.had_error:
            sys.exit(65)

        if Peu.had_runtime_error:
            sys.exit(70)

    def run_prompt(
        self,
    ) -> None:
        while True:
            line = input("> ")
            self.run(line)
            Peu.had_error = False

    @staticmethod
    def error(token: PeuToken, message: str) -> None:
        if token.type == TokenType.EOF:
            Peu.report(token.line, " at end", message)
        else:
            Peu.report(token.line, f" at '{token.lexeme}'", message)

    @staticmethod
    def report(line: int, where: str, message: str) -> None:
        sys.stderr.write(f"[line {line}] Error {where}: {message}")
        Peu.had_error = True


def main():
    peu = Peu()
    if len(sys.argv) > 2:
        print("Usage: peu [script]")
        sys.exit(64)
    elif len(sys.argv) == 2:
        peu.run_file(sys.argv[1])
    else:
        peu.run_prompt()


if __name__ == "__main__":
    main()
