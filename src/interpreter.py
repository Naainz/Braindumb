import sys
import os
from lexer import Lexer

class Interpreter:
    def __init__(self, code):
        self.lexer = Lexer(code)
        self.tokens = self.lexer.tokenize()
        self.variables = {}

    def run(self):
        self._execute_tokens()

    def _execute_tokens(self):
        while self.tokens:
            token = self.tokens.pop(0)
            print(f"Processing token: {token}")  # Debug: Show each token being processed
            if token.type == "IDENTIFIER":
                if token.value == "print!":
                    self._handle_print()
                elif token.value.startswith("red"):
                    self._handle_red_variable(token)
                else:
                    self._handle_assignment(token)
            elif token.type == "OPERATOR":
                self._handle_operator(token)

    def _handle_print(self):
        if self.tokens:
            value_token = self.tokens.pop(0)
            if value_token.type == "IDENTIFIER" and value_token.value in self.variables:
                result = self.variables[value_token.value]
                print(f"Output: {result}")  # Debug: Show what is being printed

    def _handle_red_variable(self, token):
        var_name = token.value
        if self.tokens:
            equals_token = self.tokens.pop(0)
            if equals_token.type == "OPERATOR" and equals_token.value == "=":
                if self.tokens:
                    value_token = self.tokens.pop(0)
                    if value_token.type == "NUMBER":
                        value = value_token.value
                        if value % 2 == 0:  # Ensure the value is odd
                            value += 1
                        self.variables[var_name] = value
                        print(f"Assigned {value} to {var_name} (Red Variable).")  # Debug: Show variable assignment

    def _handle_operator(self, token):
        if token.value == "*":
            if self.tokens:
                var_name = self.tokens.pop(0).value
                if self.tokens:
                    multiplier_token = self.tokens.pop(0)
                    if var_name in self.variables and multiplier_token.type == "NUMBER":
                        self.variables[var_name] *= multiplier_token.value
                        print(f"Multiplied {var_name} by {multiplier_token.value}, result is now {self.variables[var_name]}")  # Debug: Show multiplication result

    def _handle_assignment(self, token):
        var_name = token.value
        if self.tokens:
            equals_token = self.tokens.pop(0)
            if equals_token.type == "OPERATOR" and equals_token.value == "=":
                if self.tokens:
                    value_token = self.tokens.pop(0)
                    if value_token.type == "NUMBER":
                        self.variables[var_name] = value_token.value
                        print(f"Assigned {value_token.value} to {var_name}.")  # Debug: Show assignment
