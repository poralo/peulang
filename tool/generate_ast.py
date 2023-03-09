import sys
from pathlib import Path


def define_ast(output_dir: str, base_name: str, types: list[str]) -> None:
    path = Path(output_dir)
    path = path.joinpath(f"{base_name.lower()}.py")

    with open(path, "w") as f:
        f.write("from peu_token import PeuToken\n\n")
        f.write(f"class {base_name}:\n")
        f.write("    def accept(self, visitor): pass\n")

        for type in types:
            class_name = type.split(":")[0].strip()
            fields = type.split(":")[1].strip()

            class_type = define_type(base_name, class_name, fields)
            f.write(class_type)

        f.write("\n")
        visitor_type = define_visitor(base_name, types)
        f.write(visitor_type)


def define_visitor(base_name, types):
    buffer = "class Visitor:\n"
    for type in types:
        class_name = type.split(":")[0].strip()
        fields = type.split(":")[1].strip()
        buffer = f"{buffer}    def visit_{class_name.lower()}(self, {base_name.lower()}: {class_name}): raise NotImplementedError\n\n"

    return buffer


def define_type(base_name, class_name, field_list):
    fields_values = []
    for field in field_list.split(","):
        splited_field = field.strip().split(" ")
        fields_values.append((splited_field[0], splited_field[1]))

    fields = "\n        ".join(
        [
            f"self.{field_name} = {field_name}"
            for (_, field_name) in fields_values
        ]
    )
    return f"""
class {class_name}({base_name}):
    def __init__(self, {", ".join([f"{field_name}: {field_class}" for (field_class, field_name) in fields_values])}) -> None:
        super().__init__()

        {fields}

    def accept(self, visitor):
        return visitor.visit_{class_name.lower()}(self)

    def __repr__(self) -> str:
        return f"{class_name}({", ".join([f"{{self.{field_name}}}" for (_, field_name) in fields_values])})"
"""


def main():
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: python generate_ast.py <output directory>")
        sys.exit(64)

    output_dir = sys.argv[1]
    define_ast(
        output_dir,
        "Expr",
        [
            "Assign   : PeuToken name, Expr value",
            "Binary   : Expr left, PeuToken operator, Expr right",
            "Grouping : Expr expression",
            "Literal  : object value",
            "Unary    : PeuToken operator, Expr right",
            "Variable : PeuToken name",
        ],
    )

    define_ast(
        output_dir,
        "Stmt",
        [
            "Block      : list[Stmt] statements",
            "Expression : Expr expression",
            "If         : Expr condition, Stmt then_branch, Stmt else_branch",
            "Print      : Expr expression",
            "Var        : PeuToken name, Expr initializer",
        ],
    )


if __name__ == "__main__":
    main()
