import random
from lexer import Lexer

class Interpreter:
    def __init__(self, code):
        self.lexer = Lexer(code)
        self.tokens = self.lexer.tokenize()
        self.variables = {}
        self.erased_values = set()
        self.restored_values = set()

    def run(self):
        while self.tokens:
            self._process_next_command()

    def _process_next_command(self):
        if not self.tokens:
            return

        token = self.tokens.pop(0)

        if token.type == "IDENTIFIER":
            if token.value == "i":
                self._handle_inevitable_or_ironman()
            elif token.value == "print!":
                self._handle_print()
            elif token.value == "red":
                self._handle_red_variable()
            elif token.value == "green":
                self._handle_green_variable()
            elif token.value == "blue":
                self._handle_blue_variable()
            else:
                self._handle_assignment(token)

    def _handle_inevitable_or_ironman(self):
        if self.tokens and self.tokens[0].value == "am":
            self.tokens.pop(0)
            if self.tokens and self.tokens[0].value == "inevitable":
                self.tokens.pop(0)
                if self.tokens:
                    value_token = self.tokens.pop(0)
                    if value_token.type == "STRING":
                        stripped_value = value_token.value.strip("'\"")
                        self.erased_values.add(stripped_value)
                        self.restored_values.discard(stripped_value)
                    elif value_token.type == "NUMBER":
                        value_str = str(value_token.value)
                        self.erased_values.add(value_str)
                        self.restored_values.discard(value_str)
            elif self.tokens and self.tokens[0].value == "ironman":
                self.tokens.pop(0)
                if self.tokens:
                    value_token = self.tokens.pop(0)
                    if value_token.value == "*":
                        self.restored_values.update(self.erased_values)
                        self.erased_values.clear()
                    elif value_token.type in {"STRING", "NUMBER"}:
                        value_str = str(value_token.value).strip("'\"")
                        if value_str in self.erased_values:
                            self.restored_values.add(value_str)
                            self.erased_values.remove(value_str)

    def _handle_print(self):
        if self.tokens:
            value_token = self.tokens.pop(0)
            if value_token.type == "IDENTIFIER" and value_token.value in self.variables:
                result = str(self.variables[value_token.value])
                for word in self.erased_values:
                    result = result.replace(word, "")
                if result.strip() and result not in self.erased_values:
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
                        self._handle_multiplied_variable(var_token, value_token)

    def _handle_green_variable(self):
        if self.tokens:
            var_token = self.tokens.pop(0)
            if var_token.type == "IDENTIFIER" and self.tokens:
                equals_token = self.tokens.pop(0)
                if equals_token.type == "OPERATOR" and equals_token.value == "=":
                    value_token = self.tokens.pop(0)
                    if value_token.type == "NUMBER":
                        value = self._apply_magic_number_logic(value_token.value)
                        if value % 2 != 0:
                            value -= 1
                        self.variables[var_token.value] = value
                    elif value_token.type == "IDENTIFIER":
                        self._handle_multiplied_variable(var_token, value_token)

    def _handle_blue_variable(self):
        if self.tokens:
            var_token = self.tokens.pop(0)
            if var_token.type == "IDENTIFIER" and self.tokens:
                equals_token = self.tokens.pop(0)
                if equals_token.type == "OPERATOR" and equals_token.value == "=":
                    value_token = self.tokens.pop(0)
                    if value_token.type == "STRING":
                        value = value_token.value.strip("'\"")
                        if not any(vowel in value.lower() for vowel in "aeiou"):
                            value += "balls"
                        self.variables[var_token.value] = value
                    elif value_token.type == "IDENTIFIER":
                        self._handle_multiplied_variable(var_token, value_token)

    def _handle_assignment(self, token):
        var_name = token.value
        if self.tokens and self.tokens[0].type == "OPERATOR" and self.tokens[0].value == "=":
            self.tokens.pop(0)
            if self.tokens:
                value_token = self.tokens.pop(0)
                if value_token.type == "NUMBER":
                    value = self._apply_magic_number_logic(value_token.value)
                    if self.tokens and self.tokens[0].type == "OPERATOR":
                        operator = self.tokens.pop(0)
                        if operator.value == "?":
                            second_operand = self.tokens.pop(0)
                            if second_operand.type == "NUMBER":
                                value = self._apply_random_operation(value, second_operand.value)
                        elif operator.value in ["+", "-", "*", "/"]:
                            second_operand = self.tokens.pop(0)
                            if second_operand.type == "NUMBER":
                                value = self._apply_operation(value, second_operand.value, operator.value)
                    self.variables[var_name] = value
                elif value_token.type == "IDENTIFIER":
                    self._handle_multiplied_variable(token, value_token)
                elif value_token.type == "STRING":
                    value = value_token.value.strip("'\"")
                    for word in self.erased_values:
                        value = value.replace(word, "")
                    if value:
                        self.variables[var_name] = value

    def _handle_multiplied_variable(self, var_token, value_token):
        if self.tokens and self.tokens[0].type == "OPERATOR" and self.tokens[0].value == "*":
            self.tokens.pop(0)
            multiplier_token = self.tokens.pop(0)
            if multiplier_token.type == "NUMBER":
                value = self.variables.get(value_token.value, 0) * multiplier_token.value
                value = self._apply_magic_number_logic(value)
                self.variables[var_token.value] = value

    def _apply_operation(self, left_operand, right_operand, operator):
        if operator == "+":
            return left_operand + right_operand
        elif operator == "-":
            return left_operand - right_operand
        elif operator == "*":
            return left_operand * right_operand
        elif operator == "/":
            return left_operand // right_operand if right_operand != 0 else left_operand

    def _apply_random_operation(self, left_operand, right_operand):
        operation = random.choice(["+", "-", "*", "/"])
        return self._apply_operation(left_operand, right_operand, operation)

    def _apply_magic_number_logic(self, value):
        if value == 7:
            return self._get_random_prime_below_100()
        elif value == 0:
            self._invert_nearest_non_zero()
        elif value == 42:
            return "The answer to life, the universe, and everything."
        return value

    def _get_random_prime_below_100(self):
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        return random.choice(primes)

    def _invert_nearest_non_zero(self):
        for key in reversed(list(self.variables.keys())):
            if isinstance(self.variables[key], int) and self.variables[key] != 0:
                self.variables[key] = -self.variables[key]
                break
