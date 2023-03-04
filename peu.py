import sys
from scanner import Scanner

class Peu:
    had_error = False
        
    def run(self, source: str) -> None:
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        for token in tokens:
            print(token)

    def run_file(self, path: str) -> None:
        with open(path) as file:
            self.run(file.read())

        if self.had_error:
            sys.exit(65)

    def run_prompt(
        self,
    ) -> None:
        while True:
            line = input("> ")
            self.run(line)
            Peu.had_error = False

    @staticmethod
    def error(line: int, message: str) -> None:
        Peu.report(line, "", message)

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
