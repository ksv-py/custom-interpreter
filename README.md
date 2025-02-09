# Lox Interpreter

A Python implementation of the Lox programming language interpreter.

## Features

- Expression evaluation
- Variable declarations and assignments
- Print statements
- String and number literals
- Basic arithmetic operations
- Comparison operations
- Boolean operations
- Error handling with line numbers

## Grammar

```ebnf
program        → declaration* EOF ;
declaration    → varDecl | statement ;
varDecl        → "var" IDENTIFIER ( "=" expression )? ";" ;
statement      → exprStmt | printStmt ;
exprStmt       → expression ";" ;
printStmt      → "print" expression ";" ;
expression     → equality ;
equality       → comparison ( ( "!=" | "==" ) comparison )* ;
comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
term           → factor ( ( "-" | "+" ) factor )* ;
factor         → unary ( ( "/" | "*" ) unary )* ;
unary          → ( "!" | "-" ) unary | primary ;
primary        → NUMBER | STRING | "true" | "false" | "nil"
               | "(" expression ")" | IDENTIFIER ;
```

## Run a Lox file
```
python main.py run test.lox
```

## Example Lox program
```
print 9 + 4;
```

## Strings
```
print "Hello, " + "world"; 
```

## Boolean operations
```
print !True;
```
