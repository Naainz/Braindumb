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
            elif char in ["'", '"']:  # Handle strings
                self.tokens.append(self._tokenize_string())
            elif char.isdigit():
                self.tokens.append(self._tokenize_number())
            elif char.isalpha() or char == '_':
                self.tokens.append(self._tokenize_identifier())
            elif char in "=+*/-":
                self.tokens.append(Token("OPERATOR", char))
                self.current_position += 1
            elif char in "!":
                self.tokens.append(Token("EMOTION", char + self._tokenize_emotion()))
            else:
                self.current_position += 1

        return self.tokens

    def _tokenize_string(self):
        quote_type = self.code[self.current_position]
        self.current_position += 1
        string_value = ''
        while self.current_position < len(self.code) and self.code[self.current_position] != quote_type:
            string_value += self.code[self.current_position]
            self.current_position += 1
        self.current_position += 1  # Skip closing quote
        return Token("STRING", string_value)

    def _tokenize_number(self):
        number_value = ''
        while self.current_position < len(self.code) and self.code[self.current_position].isdigit():
            number_value += self.code[self.current_position]
            self.current_position += 1
        return Token("NUMBER", int(number_value))

    def _tokenize_identifier(self):
        identifier_value = ''
        while self.current_position < len(self.code) and (self.code[self.current_position].isalnum() or self.code[self.current_position] == '_'):
            identifier_value += self.code[self.current_position]
            self.current_position += 1
        return Token("IDENTIFIER", identifier_value)

    def _tokenize_emotion(self):
        emotion_value = ''
        self.current_position += 1
        while self.current_position < len(self.code) and self.code[self.current_position].isalpha():
            emotion_value += self.code[self.current_position]
            self.current_position += 1
        return emotion_value
