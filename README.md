# peulang
Le peulang, le nouveau langage de programmation à la mode.

## La grammaire
- Littéraux : Nombres, strings, booleans et null.
- Expressions unaires : Le préfix ! pour permettre le non logique et le - pour les nombres négatifs.
- Expressions binaires : Les opérateurs arithmétiques (+, -, *, /) et logiques (==, !=, <, <=, >, >=).
- Parenthèses : Une paire de ( et ) entourant une expression.

Un exemple d'expression :
> 1 - (2 * 3) < 4 == false

La grammaire devient donc :
> expression     → literal | unary | binary | grouping ;
> literal        → NUMBER | STRING | "true" | >"false" | "nil" ;
>grouping       → "(" expression ")" ;
>unary          → ( "-" | "!" ) expression ;
>binary         → expression operator expression ;
>operator       → "==" | "!=" | "<" | "<=" | ">" | ">=" | "+"  | "-"  | "*" | "/" ;