import sys
import os
from lexer import Lexer

class Interpreter:
    def __init__(self, code):
        self.lexer = Lexer(code)
        self.tokens = self.lexer.tokenize()
        self.variables = {}

    def run(self):
        print("Interpreter is running...")
        self._execute_tokens()

    def _execute_tokens(self):
        while self.tokens:
            token = self.tokens.pop(0)
            print(f"Processing token: {token}")
            if token.type == "IDENTIFIER":
                if token.value == "print!":
                    self._handle_print()
                elif token.value.startswith("red"):
                    self._handle_red_variable(token)
                else:
                    self._handle_assignment(token)
            elif token.type == "OPERATOR":
                self._handle_operator(token)
            elif token.type == "EMOTION":
                print(f"Ignoring emotion token: {token.value}")
            else:
                print(f"Unknown token type: {token.type} with value {token.value}")

    def _handle_print(self):
        print("Handling print statement...")
        if self.tokens:
            value_token = self.tokens.pop(0)
            if value_token.type == "IDENTIFIER" and value_token.value in self.variables:
                result = self.variables[value_token.value]
                print(f"Result: {result}")

    def _handle_red_variable(self, token):
        print("Handling red variable assignment...")
        var_name = token.value
        if self.tokens and self.tokens[0].type == "OPERATOR" and self.tokens[0].value == "=":
            self.tokens.pop(0)  # Consume the '=' token
            if self.tokens:
                value_token = self.tokens.pop(0)
                if value_token.type == "NUMBER":
                    value = value_token.value
                    if value % 2 == 0:  # Ensure the value is odd
                        value += 1
                    self.variables[var_name] = value
                    print(f"Assigned {var_name} = {value}")
        else:
            print(f"Unexpected token after red: {self.tokens[0] if self.tokens else 'None'}")

    def _handle_operator(self, token):
        print("Handling operator...")
        if token.value == "*":
            if self.tokens:
                var_name = self.tokens.pop(0).value
                if self.tokens:
                    multiplier_token = self.tokens.pop(0)
                    if var_name in self.variables and multiplier_token.type == "NUMBER":
                        original_value = self.variables[var_name]
                        self.variables[var_name] *= multiplier_token.value
                        print(f"{var_name} = {original_value} * {multiplier_token.value}  # Result is now {self.variables[var_name]}")

    def _handle_assignment(self, token):
        print("Handling assignment...")
        var_name = token.value
        if self.tokens and self.tokens[0].type == "OPERATOR" and self.tokens[0].value == "=":
            self.tokens.pop(0)  # Consume the '=' token
            if self.tokens:
                value_token = self.tokens.pop(0)
                if value_token.type == "NUMBER":
                    self.variables[var_name] = value_token.value
                    print(f"Assigned {var_name} = {value_token.value}")
                elif value_token.type == "IDENTIFIER":
                    if self.tokens and self.tokens[0].type == "OPERATOR" and self.tokens[0].value == "*":
                        self.tokens.pop(0)  # Consume the '*' token
                        if self.tokens:
                            multiplier_token = self.tokens.pop(0)
                            if multiplier_token.type == "NUMBER" and value_token.value in self.variables:
                                self.variables[var_name] = self.variables[value_token.value] * multiplier_token.value
                                print(f"{var_name} = {self.variables[value_token.value]} * {multiplier_token.value}  # Result is now {self.variables[var_name]}")
        else:
            print(f"Unexpected token after assignment: {self.tokens[0] if self.tokens else 'None'}")
