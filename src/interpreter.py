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
                elif token.value == "red":
                    self._handle_red_variable()
                else:
                    self._handle_assignment(token)
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
            else:
                print(f"Expected identifier after print!, but found: {value_token}")

    def _handle_red_variable(self):
        print("Handling red variable assignment...")
        if self.tokens:
            var_token = self.tokens.pop(0)  # Get the variable name
            if var_token.type == "IDENTIFIER":
                if self.tokens:
                    equals_token = self.tokens.pop(0)  # Get the '='
                    if equals_token.type == "OPERATOR" and equals_token.value == "=":
                        value_token = self.tokens.pop(0)
                        if value_token.type == "NUMBER":
                            value = value_token.value
                            if value % 2 == 0:
                                value += 1  # Ensure the value is odd
                            self.variables[var_token.value] = value
                            print(f"Assigned {var_token.value} = {value}")
                        elif value_token.type == "IDENTIFIER":
                            if self.tokens and self.tokens[0].type == "OPERATOR" and self.tokens[0].value == "*":
                                self.tokens.pop(0)  # Consume the '*' token
                                multiplier_token = self.tokens.pop(0)
                                if multiplier_token.type == "NUMBER":
                                    self.variables[var_token.value] = self.variables[value_token.value] * multiplier_token.value
                                    print(f"{var_token.value} = {self.variables[value_token.value]} * {multiplier_token.value}  # Result is now {self.variables[var_token.value]}")
                            else:
                                print(f"Expected operator after {value_token.value}")
                        else:
                            print(f"Unexpected token after '=': {value_token}")
                    else:
                        print(f"Expected '=', but found: {equals_token}")
            else:
                print(f"Expected identifier after 'red', but found: {var_token}")

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
                        multiplier_token = self.tokens.pop(0)
                        if multiplier_token.type == "NUMBER":
                            self.variables[var_name] = self.variables[value_token.value] * multiplier_token.value
                            print(f"{var_name} = {self.variables[value_token.value]} * {multiplier_token.value}  # Result is now {self.variables[var_name]}")
                    else:
                        self.variables[var_name] = self.variables.get(value_token.value, 0)
                        print(f"Assigned {var_name} = {self.variables[var_name]} (from identifier {value_token.value})")
                else:
                    print(f"Unexpected token after assignment: {value_token}")
            else:
                print(f"Assignment complete.")
        else:
            print(f"Unexpected token after assignment: {self.tokens[0] if self.tokens else 'None'}")

        # After handling the assignment, return to ensure the next command starts fresh
        return
