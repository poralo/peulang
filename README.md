# peulang
Le peulang, le nouveau langage de programmation à la mode.

```
program        → statement* EOF ;

statement      → exprStmt
               | ifStmt
               | printStmt 
               | block ;

exprStmt       → expression ";" ;
ifStmt         → "if" "(" expression ")" statement ( "else" statement )? ;
printStmt      → "print" expression ";" ;
block          → "{" declaration* "}" ;

expression     → assignment ;
assignment     → IDENTIFIER "=" assignment
               | logic_or ;
logic_or       → logic_and ( "or" logic_and )* ;
logic_and      → equality ( "and" equality )* ;
```

## La grammaire
- Littéraux : Nombres, strings, booleans et null.
- Expressions unaires : Le préfix ! pour permettre le non logique et le - pour les nombres négatifs.
- Expressions binaires : Les opérateurs arithmétiques (+, -, *, /) et logiques (==, !=, <, <=, >, >=).
- Parenthèses : Une paire de ( et ) entourant une expression.

Un exemple d'expression :
`1 - (2 * 3) < 4 == false`

La grammaire devient donc :
```
expression     → literal | unary | binary | grouping ;
literal        → NUMBER | STRING | "true" | "false" | "nil" ;
grouping       → "(" expression ")" ;
unary          → ( "-" | "!" ) expression ;
binary         → expression operator expression ;
operator       → "==" | "!=" | "<" | "<=" | ">" | ">=" | "+"  | "-"  | "*" | "/" ;
```