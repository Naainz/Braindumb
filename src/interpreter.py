import sys
import os
from lexer import Lexer

class Interpreter:
    def __init__(self, code):
        self.lexer = Lexer(code)
        self.tokens = self.lexer.tokenize()
        self.variables = {}
        self.erased_values = set()

    def run(self):
        while self.tokens:
            self._process_next_command()

    def _process_next_command(self):
        if not self.tokens:
            return

        token = self.tokens.pop(0)

        if token.type == "IDENTIFIER":
            if token.value == "i":
                self._handle_inevitable()
            elif token.value == "print!":
                self._handle_print()
            elif token.value == "red":
                self._handle_red_variable()
            else:
                self._handle_assignment(token)

    def _handle_inevitable(self):
        if self.tokens and self.tokens[0].value == "am":
            self.tokens.pop(0)
            if self.tokens and self.tokens[0].value == "inevitable":
                self.tokens.pop(0)
                if self.tokens:
                    value_token = self.tokens.pop(0)
                    if value_token.type == "STRING":
                        stripped_value = value_token.value.strip("'\"")
                        self.erased_values.add(stripped_value)
                    elif value_token.type == "NUMBER":
                        self.erased_values.add(str(value_token.value))  # Store as string for comparison

    def _handle_print(self):
        if self.tokens:
            value_token = self.tokens.pop(0)
            if value_token.type == "IDENTIFIER" and value_token.value in self.variables:
                result = str(self.variables[value_token.value])
                for word in self.erased_values:
                    result = result.replace(word, "")
                print(result.strip())

    def _handle_red_variable(self):
        if self.tokens:
            var_token = self.tokens.pop(0)
            if var_token.type == "IDENTIFIER" and self.tokens:
                equals_token = self.tokens.pop(0)
                if equals_token.type == "OPERATOR" and equals_token.value == "=":
                    value_token = self.tokens.pop(0)
                    if value_token.type == "NUMBER":
                        value = value_token.value
                        if value % 2 == 0:
                            value += 1
                        self.variables[var_token.value] = value
                    elif value_token.type == "IDENTIFIER":
                        if self.tokens and self.tokens[0].type == "OPERATOR" and self.tokens[0].value == "*":
                            self.tokens.pop(0)
                            multiplier_token = self.tokens.pop(0)
                            if multiplier_token.type == "NUMBER":
                                self.variables[var_token.value] = self.variables[value_token.value] * multiplier_token.value

    def _handle_assignment(self, token):
        var_name = token.value
        if self.tokens and self.tokens[0].type == "OPERATOR" and self.tokens[0].value == "=":
            self.tokens.pop(0)
            if self.tokens:
                value_token = self.tokens.pop(0)
                if value_token.type == "NUMBER":
                    value_str = str(value_token.value)
                    for word in self.erased_values:
                        value_str = value_str.replace(word, "")
                    if value_str:
                        self.variables[var_name] = int(value_str)
                elif value_token.type == "IDENTIFIER":
                    if self.tokens and self.tokens[0].type == "OPERATOR" and self.tokens[0].value == "*":
                        self.tokens.pop(0)
                        multiplier_token = self.tokens.pop(0)
                        if multiplier_token.type == "NUMBER":
                            result = self.variables[value_token.value] * multiplier_token.value
                            result_str = str(result)
                            for word in self.erased_values:
                                result_str = result_str.replace(word, "")
                            if result_str:
                                self.variables[var_name] = int(result_str)
                    else:
                        value = self.variables.get(value_token.value, 0)
                        value_str = str(value)
                        for word in self.erased_values:
                            value_str = value_str.replace(word, "")
                        if value_str:
                            self.variables[var_name] = int(value_str)
                elif value_token.type == "STRING":
                    value = value_token.value.strip("'\"")
                    for word in self.erased_values:
                        value = value.replace(word, "")
                    if value:
                        self.variables[var_name] = value
