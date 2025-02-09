import sys

def tokenize_file(file_contents):
    # Reserved words in the language (keywords)
    reserved_words = {
        "and", "class", "else", "false", "for", "fun", "if", "nil", "or", "print", 
        "return", "super", "this", "true", "var", "while"
    }

    # Mapping of single-character symbols to token types
    token_map = {
        "(": "LEFT_PAREN",
        ")": "RIGHT_PAREN",
        "{": "LEFT_BRACE",
        "}": "RIGHT_BRACE",
        ",": "COMMA",
        ".": "DOT",
        "-": "MINUS",
        "+": "PLUS",
        ";": "SEMICOLON",
        "*": "STAR"
    }

    tokens = []  # List to hold all the tokens
    error = False  # Flag to indicate errors during tokenization
    unterminated_string = False
    i = 0  # Pointer to iterate over the file contents

    while i < len(file_contents):  # Iterate through the file contents
        c = file_contents[i]  # Current character in the file

        # Skip whitespace characters (space, carriage return, tab, newline)
        if c in " \r\t\n":
            ...

        # Handle single-character symbols (e.g., parentheses, operators)
        elif c in "(){},.-+;*":
            token = {"type": token_map[c], "value": c}
            tokens.append(token)  # Add the token to the list

        # Handle operators and other special symbols (e.g., ==, !=)
        elif c == "=":
            if i + 1 < len(file_contents) and file_contents[i + 1] == "=":
                token = {"type": "EQUAL_EQUAL", "value": "=="}
                i += 1  # Skip the second '=' character
            else:
                token = {"type": "EQUAL", "value": "="}
            tokens.append(token)  # Add the token to the list

        # Handle reserved words (keywords) and identifiers
        # Add logic for reserved words, identifiers, strings, numbers, etc.

        # Move to the next character
        # Handle less-than or less-than-equal (<=)
        elif c == "<":
            if i + 1 < len(file_contents) and file_contents[i + 1] == "=":
                token = {"type": "LESS_EQUAL", "value": "<="}
                i += 1  # Skip the '=' character
            else:
                token = {"type": "LESS", "value": "<"}
            tokens.append(token)  # Add the token to the list

        # Handle greater-than or greater-than-equal (>=)
        elif c == ">":
            if i + 1 < len(file_contents) and file_contents[i + 1] == "=":
                token = {"type": "GREATER_EQUAL", "value": ">="}
                i += 1  # Skip the '=' character
            else:
                token = {"type": "GREATER", "value": ">"}
            tokens.append(token)  # Add the token to the list

        # Handle not-equal (!=) or not (!) 
        elif c == "!":
            if i + 1 < len(file_contents) and file_contents[i + 1] == "=":
                token = {"type": "BANG_EQUAL", "value": "!="}
                i += 1  # Skip the '=' character
            else:
                token = {"type": "BANG", "value": "!"}
            tokens.append(token)  # Add the token to the list

        # Handle comments (//) – Skip the rest of the line after '//'
        elif c == "/":
            if i + 1 < len(file_contents) and file_contents[i + 1] == "/":
                while i < len(file_contents) and file_contents[i] != "\n":
                    i += 1  # Skip characters until the end of the line
            else:
                token = {"type": "SLASH", "value": "/"}
                tokens.append(token)  # Add the token to the list

        # Handle string literals (enclosed in " or ')
        elif c in "\"'":
            quote_type = c  # Keep track of whether it's a single or double quote
            i += 1  # Move to the next character after the opening quote
            string_value = ""  # Initialize an empty string for the literal value
            while i < len(file_contents) and file_contents[i] != quote_type:
                string_value += file_contents[i]  # Append characters inside the string literal 
                i += 1
            if i == len(file_contents):  # Error: Unterminated string literal
                error = True
                unterminated_string = True
                line_no = file_contents.count("\n", 0, i) + 1
                print(f"[line {line_no}] Error: Unterminated string.", file=sys.stderr)
            else:
                token = {"type": "STRING", "value": string_value}  # Create a token for the string
                tokens.append(token)  # Add the token to the list

        # Handle numbers (integers and floats)
        elif c.isdigit():
            start_idx = i  # Mark the starting index of the number
            while i < len(file_contents) and (file_contents[i].isdigit() or file_contents[i] == "."):
                i += 1  # Move until the end of the number
            lexeme = file_contents[start_idx:i]
            
            # Extract the lexeme (the number string)
            # Check for invalid number literals (multiple decimal points or non-numeric characters)
            if lexeme.count(".") > 1 or not lexeme.replace(".", "", 1).isdigit():
                error = True
                line_no = file_contents.count("\n", 0, i) + 1
                print(f"[line {line_no}] Error: Invalid number literal.", file=sys.stderr)
            else:
                token = {"type": "NUMBER", "value": float(lexeme), 'lexeme':lexeme}  # Create a token for the number
                tokens.append(token)  # Add the token to the list
            i-=1

        # Handle identifiers (variable names, function names, etc.)
        elif c.isalpha() or c == "_":
            start_idx = i  # Mark the starting index of the identifier
            while i < len(file_contents) and (file_contents[i].isalnum() or file_contents[i] == "_"):
                i += 1  # Move until the end of the identifier
            lexeme = file_contents[start_idx:i]  # Extract the lexeme (the identifier)
            i-=1
            if lexeme in reserved_words:  # Check if it's a reserved word (keyword)
                token = {"type": lexeme.upper(), "value": lexeme}  # Reserved word token
                tokens.append(token)  # Add the token to the list
            else:
                token = {"type": "IDENTIFIER", "value": lexeme}  # Regular identifier token
                tokens.append(token)  # Add the token to the list

        # Handle unexpected characters (errors)
        else:
            error = True
            # unexpected_error = True
            line_no = file_contents.count("\n", 0, i) + 1
            print(f"[line {line_no}] Error: Unexpected character: {c}", file=sys.stderr)


        i += 1  # Move to the next character

    # Add an EOF (End of File) token
    if len(tokens) >= 1 or not unterminated_string:
        tokens.append({"type": "EOF", "value": "null"})

    # print(tokens)
    # If there was an error, exit with code 65
    return tokens, error  # Return the list of tokens

def print_tokens(tokens):
    for token in tokens:
        if token['type'] == 'EOF':
            print(f"{token['type']}  {token['value']}")
        elif token['type'] == 'STRING':
            print(f"{token['type']} \"{token['value']}\" {token['value']}")
        elif token['type'] == 'NUMBER':
            print(f"{token['type']} {(token['lexeme'])} {token['value']}")
        else:
            print(f"{token['type']} {token['value']} null")
 
def literals(value):
    if value is None:
        return {'type': 'literal', 'value': 'nil'}
    return {'type': 'literal', 'value': str(value).lower()}

def unary(operator, right):
    return {'type': 'unary', 'operator': operator, 'right': right}

def binary(left, operator, right):
    return {'type': 'binary', 'operator': operator, 'left': left, 'right': right}

def grouping(expression):
    return {'type': 'grouping', 'expression': expression}

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0  # Points to the current token

    def parse(self):
        statements = []
        while not self.is_at_end():
            statements.append(self.statement())  # Parse multiple statements
        return statements  

    def statement(self):
        if self.match("PRINT"):
            return self.print_statement()
        return self.expression()  # If it's not a print statement, parse it as an expression

    def print_statement(self):
        value = self.expression()  # Parse the expression inside print
        self.consume("SEMICOLON", "Expect ';' after value.","65")  # Ensure print ends with ';'
        return {"type": "print", "value": value}
    
    def expression(self):
        return self.equality()
    
    def equality(self):
        expr = self.comparison()
        while self.match("BANG_EQUAL", "EQUAL_EQUAL"):
            operator = self.previous()
            right = self.comparison()
            expr = binary(expr, operator["value"], right)
        return expr

    def comparison(self):
        expr = self.term()
        while self.match("GREATER", "GREATER_EQUAL", "LESS", "LESS_EQUAL"):
            operator = self.previous()
            right = self.term()
            expr = binary(expr, operator["value"], right)
        return expr
    

    def term(self):
        expr = self.factor()
        while self.match("MINUS", "PLUS"):
            operator = self.previous()
            right = self.factor()
            expr = binary(expr, operator["value"], right)
        return expr
    
    def factor(self):
        expr = self.unary()
        while self.match("SLASH", "STAR"):
            operator = self.previous()
            right = self.unary()
            expr = binary(expr, operator["value"], right)
        return expr

    def unary(self):
        if self.match("BANG", "MINUS"):
            operator = self.previous()
            right = self.unary()
            return unary(operator["value"], right)
        return self.primary()

    def primary(self):
        if self.match("FALSE"):
            return literals(False)
        if self.match("TRUE"):
            return literals(True)
        if self.match("NIL"):
            return literals(None)
        if self.match("NUMBER"):
            return self.previous()["value"]
        if self.match("STRING"):
            return self.previous()["value"]
        if self.match("LEFT_PAREN"):
            expr = self.expression() # {'type': 'binary', 'operator': '!=', 'left': '92', 'right': '56'}
            self.consume("RIGHT_PAREN", "Expect ')' after expression.")
            return grouping(expr)
        if self.match("IDENTIFIER"):
            return {"type": "IDENTIFIER", "value": self.previous()["value"]}
        if self.match("SEMICOLON"):
            return None
        self.error("Expect expression.")


    def print_ast(self, expr):
        if isinstance(expr, list):
            for statement in expr:
                return self.print_ast(statement)
        if isinstance(expr, dict):
                if expr['type'] == 'binary':
                    return f"({expr['operator']} {self.print_ast(expr['left'])} {self.print_ast(expr['right'])})"
                elif expr['type'] == 'grouping':
                    return f"(group {self.print_ast(expr['expression'])})"
                elif expr['type'] == 'unary':
                    return f"({expr['operator']} {self.print_ast(expr['right'])})"
                elif expr['type'] == 'literal':
                    return expr['value']
        elif isinstance(expr, (str,int,float)):
            return expr
        return ""


    # Utility Methods
    def match(self, *types):
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def check(self, token_type):
        if self.is_at_end():
            return False
        return self.peek()["type"] == token_type

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self):
        return self.peek()["type"] == "EOF"

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]
        
    def consume(self, token_type, message,*ext_code):
        if self.check(token_type):
            return self.advance()
        if message == "Expect ';' after value.":
            sys.exit(65)
        self.error(message)

    def error(self, message,*ext_code):
        token = self.peek()
        line = token.get("line", "unknown")
        raise SyntaxError(f"[line {line}] Error: {message}")

class Evaluator:
    def d_type(self, value):
        if value.is_integer():
            return int(value)
        return value
    
    def evaluate(self, expr):
        arithmetic = {'+': lambda x, y: x + y, 
                      '-': lambda x, y: x - y, 
                      '*': lambda x, y: x * y, 
                      '/': lambda x, y: x / y}
        comparison = ['>', '>=', '<', '<=', '==', '!=']
        if isinstance(expr, list):
            for statement in expr:
                eval_statement = self.evaluate(statement)
            return eval_statement #heres the problem
        if isinstance(expr, dict):
            if expr['type'] == 'print':
                print(self.evaluate(expr['value']))
                return None
            
            if expr['type'] == 'literal':
                if expr['value'] == 'true':
                    return 'true'
                elif expr['value'] == 'false':
                    return 'false'
                elif expr['value'] == 'nil':
                    return 'nil'
                elif float(expr['value']).is_integer():
                    return int(expr['value'])
                return expr['value']

            elif expr['type'] == 'binary':
                left = self.evaluate(expr['left'])
                # try printing dtype of left and right
                right = self.evaluate(expr['right'])
                operator = expr['operator']
                
                if isinstance(left, str) or isinstance(right,str):
                    if operator == '==' and (isinstance(left, str) or isinstance(right, str)):
                        return str(left == right).lower()
                    if operator == '!=' and (isinstance(left, str) or isinstance(right, str)):
                        return str(left != right).lower()
                    if right in ['true','false'] or left in ['true','false']:
                        raise SyntaxError(f"Operand must be two numbers or two strings.")
                    if operator == '+' and (isinstance(left, str) and isinstance(right, str)):
                        return str(left) + str(right)  #concatenate strings
                    else:
                        raise RuntimeError(f"Operand must be a number.")

                
                elif operator in arithmetic:
                    # if operator in ['/','*']:
                    #     if isinstance(right,(str,bool)) or isinstance(left,(str,bool)):
                    #         raise SyntaxError(f"Operand must be a number.")
                    return self.d_type(arithmetic[operator](float(left), float(right)))
                
                elif operator in comparison:
                    if operator == '>':
                        return (left > right).__str__().lower()
                    elif operator == '>=':
                        return (left >= right).__str__().lower()
                    elif operator == '<':
                        return (left < right).__str__().lower()
                    elif operator == '<=':
                        return (left <= right).__str__().lower()
                    elif operator == '==':
                        if type(left) != type(right):
                            return 'false'
                        return (left == right).__str__().lower()
                    elif operator == '!=':
                        if type(left) != type(right):
                            return 'true'
                        return (left != right).__str__().lower()
                else:
                    raise SyntaxError(f"Operand must be two numbers or two strings.")
            elif expr['type'] == 'grouping':
                return self.evaluate(expr['expression'])
                
            elif expr['type'] == 'unary':
                right = self.evaluate(expr['right'])
                operator = expr['operator']
                
                if operator == '-':
                    if not isinstance(right, (int, float)):
                        raise RuntimeError(f"Operand must be a number.")
                    num = float(right)
                    if isinstance(num, float) and num.is_integer():
                        return -int(num)
                    return -float(right)
                elif operator == '!':
                    if right == 'false' or right == 'nil':
                        return 'true'
                    elif right == 'true':
                        return 'false'
                    else:
                        return 'false'
        else:
            try:
                if expr.is_integer():
                    return int(expr)
                elif expr.is_float():
                    return float(expr)
                elif expr.is_string():
                    return expr
            except:
                return expr

def main():
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh <command> <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    try:
        with open(filename, encoding="utf-8") as file:
            file_contents = file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.", file=sys.stderr)
        exit(1)

    tokens,error = tokenize_file(file_contents)
    parser = Parser(tokens)
    
    if error:
        print_tokens(tokens)
        sys.exit(65)

    if command == "tokenize":
        print_tokens(tokens)
    

    elif command == "parse":
        parser = Parser(tokens)
        try:
            expression = parser.parse()  # Generate the AST
            print(parser.print_ast(expression))  # Print the AST representation
        except Exception as e:
            print(e, file=sys.stderr)
            sys.exit(65)

    elif command == "evaluate":
        parser = Parser(tokens)
        try:
            expression = parser.parse()
            evaluator = Evaluator()
            result = evaluator.evaluate(expression)
            
            print(result)
        except Exception as e:
            print(f"Error: {str(e)}", file=sys.stderr)
            sys.exit(70)

    elif command == 'run':
        parser = Parser(tokens)
        try:
            expression = parser.parse()
            evaluator = Evaluator()
            result = evaluator.evaluate(expression)
        except Exception as e:
            print(f"Error: {str(e)}", file=sys.stderr)
            sys.exit(70)

    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)
    
if __name__ == "__main__":
    main()


