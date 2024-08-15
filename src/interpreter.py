#!/usr/bin/env python3

import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from lexer import Lexer

class Interpreter:
    def __init__(self, code):
        self.lexer = Lexer(code)
        self.tokens = self.lexer.tokenize()
        self.variables = {}
        self.deleted_items = set()

    def run(self):
        self._execute_tokens()

    def _execute_tokens(self):
        for token in self.tokens:
            if token.type == "IDENTIFIER":
                if token.value == "noctiufn":
                    self._handle_function_definition()
                elif token.value == "print!":
                    self._handle_print()
                elif token.value.startswith("I am inevitable"):
                    self._handle_inevitable()
                elif token.value.startswith("And I am Ironman"):
                    self._handle_ironman()
                else:
                    self._handle_assignment(token)
    
    def _handle_function_definition(self):
        print("Defining a function... (not actually implemented)")

    def _handle_print(self):
        value_token = self.tokens.pop(0)
        if value_token.type == "STRING":
            if "!" in value_token.value:
                value = value_token.value.strip('"').upper()
            else:
                value = value_token.value.strip('"')
            print(value)
        elif value_token.type == "NUMBER":
            if value_token.value in self.deleted_items:
                print(f"Error: {value_token.value} doesn't exist.")
            else:
                print(value_token.value)
    
    def _handle_inevitable(self):
        inevitable_token = self.tokens.pop(0)
        if inevitable_token.type == "NUMBER" or inevitable_token.type == "STRING":
            self.deleted_items.add(inevitable_token.value)
            print(f"Deleted {inevitable_token.value} from existence.")
    
    def _handle_ironman(self):
        ironman_token = self.tokens.pop(0)
        if ironman_token.value in self.deleted_items:
            self.deleted_items.remove(ironman_token.value)
            print(f"Restored {ironman_token.value} to existence.")
    
    def _handle_assignment(self, token):
        
        if token.type == "IDENTIFIER":
            var_name = token.value
            equals_token = self.tokens.pop(0)
            if equals_token.type == "OPERATOR" and equals_token.value == "=":
                value_token = self.tokens.pop(0)
                if value_token.type == "NUMBER" or value_token.type == "STRING":
                    self.variables[var_name] = value_token.value
                    print(f"Assigned {value_token.value} to {var_name}.")
