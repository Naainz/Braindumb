import re

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"{self.type}({self.value})"

class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.current_position = 0

    def tokenize(self):
        while self.current_position < len(self.code):
            char = self.code[self.current_position]

            if char.isspace():
                self.current_position += 1
            elif char.isdigit():
                self.tokens.append(self._tokenize_number())
            elif char.isalpha() or char in ["'", '"', "!", "?"]:
                self.tokens.append(self._tokenize_identifier_or_string())
            elif char in "=+*/-":
                self.tokens.append(Token("OPERATOR", char))
                self.current_position += 1
            elif char == '(' or char == ')':
                
                self.current_position += 1
            elif char == '📂':
                self.tokens.append(Token("FILE", "📂"))
                self.current_position += 1
            else:
                self.current_position += 1

        return self.tokens

    def _tokenize_number(self):
        number = ''
        while self.current_position < len(self.code) and self.code[self.current_position].isdigit():
            number += self.code[self.current_position]
            self.current_position += 1
        return Token("NUMBER", int(number))

    def _tokenize_identifier_or_string(self):
        id_str = ''
        while self.current_position < len(self.code) and (
            self.code[self.current_position].isalnum() or self.code[self.current_position] in ["'", '"', "!", "?"]
        ):
            id_str += self.code[self.current_position]
            self.current_position += 1
        if id_str[0] in ["'", '"']:
            return Token("STRING", id_str)
        elif "!" in id_str or "?" in id_str:
            return Token("EMOTION", id_str)
        return Token("IDENTIFIER", id_str)
