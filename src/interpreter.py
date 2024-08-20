import random
from lexer import Lexer
from num2words import num2words
from word2number import w2n

class Interpreter:
    def __init__(self, code):
        self.lexer = Lexer(code)
        self.tokens = self.lexer.tokenize()
        self.variables = {}
        self.erased_values = set()
        self.restored_values = set()
        self.poop_emoji_active = False

    def run(self):
        while self.tokens:
            self._process_next_command()

    def _process_next_command(self):
        if not self.tokens:
            return

        token = self.tokens.pop(0)

        if token.type == "IDENTIFIER":
            self._handle_identifier(token)
        elif token.type == "EMOJI":
            self._handle_emoji(token)

    def _handle_identifier(self, token):
        if self.poop_emoji_active:
            self._apply_poop_logic(token.value)

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
        elif "at position" in token.value:
            self._handle_array_position_access(token)
        else:
            self._handle_assignment(token)

    def _handle_emoji(self, token):
        if token.value == "💩":
            self.poop_emoji_active = True

    def _apply_poop_logic(self, var_name):
        if var_name in self.variables and isinstance(self.variables[var_name], int):
            value = self.variables[var_name]
            if value % 3 == 0:
                self.variables[var_name] = value * 2
        self.poop_emoji_active = False

    def _handle_array_position_access(self, token):
        array_name, index_str = token.value.split(" at position ")
        index = int(index_str.strip())
        adjusted_index = (index + 2) // 2  # Adjust index according to -2, 0, 2, 4, ...

        if array_name in self.variables and adjusted_index < len(self.variables[array_name]):
            value = self.variables[array_name][adjusted_index]
            if value is not None:
                self.variables["my_array_value"] = value  # Store the value in my_array_value
            else:
                self._print_error(f"Error: Array '{array_name}' at position {index} is not initialized.", array_name)
        else:
            self._print_error(f"Error: Array '{array_name}' does not have a valid position {index}.", array_name)

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
            if value_token.type == "IDENTIFIER":
                if value_token.value in self.variables:
                    result = str(self.variables[value_token.value])
                    for word in self.erased_values:
                        result = result.replace(word, "")
                    if result.strip() and result not in self.erased_values:
                        print(result.strip())
                elif "at position" in value_token.value:
                    array_name, index_str = value_token.value.split(" at position ")
                    index = int(index_str.strip())
                    adjusted_index = (index + 2) // 2
                    if array_name in self.variables and adjusted_index < len(self.variables[array_name]):
                        result = self.variables[array_name][adjusted_index]
                        if result is not None:
                            print(result)
                        else:
                            self._print_error(f"Error: Array '{array_name}' at position {index} is not initialized.", array_name)
                    else:
                        self._print_error(f"Error: Array '{array_name}' does not have a valid position {index}.", array_name)
                else:
                    self._print_warning(f"Variable '{value_token.value}' is not initialized.", value_token.value)

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
                    value = value_token.value
                    if value > 999:
                        spelled_value = num2words(value).replace("-", " ").replace(",", "")
                        self._print_error(f"Error: Number {value} must be spelled out as '{spelled_value}'.", var_name)
                        return
                    value = self._apply_magic_number_logic(value)
                    if self.tokens and self.tokens[0].type == "OPERATOR":
                        operator = self.tokens.pop(0)
                        second_operand = None
                        if operator.value == "?":
                            second_operand = self.tokens.pop(0)
                            if second_operand.type == "NUMBER":
                                value = self._apply_random_operation(value, second_operand.value)
                        elif operator.value in ["+", "-", "*", "/"]:
                            second_operand = self.tokens.pop(0)
                            if operator.value == "/" and second_operand.value == 0:
                                self._print_warning("Division by zero is not allowed.", var_name)
                                return
                            if second_operand.type == "NUMBER":
                                value = self._apply_operation(value, second_operand.value, operator.value)
                    self.variables[var_name] = value
                elif value_token.type == "STRING":
                    spelled_out_number = self._words_to_number(value_token.value.strip("'\""))
                    if spelled_out_number is not None:
                        value = spelled_out_number
                    else:
                        value = value_token.value.strip("'\"")
                    for word in self.erased_values:
                        value = value.replace(word, "")
                    if value:
                        self.variables[var_name] = value
                elif value_token.type == "IDENTIFIER":
                    if value_token.value not in self.variables:
                        self._print_warning(f"Variable '{value_token.value}' is not initialized.", var_name)
                    else:
                        self.variables[var_name] = self.variables[value_token.value]

    def _words_to_number(self, words):
        try:
            return w2n.word_to_num(words)
        except ValueError:
            return None

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
            if right_operand == 0:
                self._print_warning("Division by zero is not allowed.", left_operand)
                return left_operand
            return left_operand // right_operand

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

    def _print_error(self, message, var_name):
        penguin_fact = self._get_random_penguin_fact()
        error_message = f"{message} Here's a penguin fact: {penguin_fact}"
        self._output_message(error_message, var_name)

    def _print_warning(self, message, var_name=None):
        motivational_quote = self._get_random_motivational_quote()
        warning_message = f"Motivational Quote: {motivational_quote}"
        self._output_message(warning_message, var_name)

    def _output_message(self, message, var_name):
        if var_name and self._is_palindrome(var_name):
            message = message[::-1]
        print(message)

    def _is_palindrome(self, word):
        return word == word[::-1]

    def _get_random_penguin_fact(self):
        facts = [
            "Penguins can dive as deep as 1,850 feet.",
            "A group of penguins in the water is called a 'raft', but on land, they're called a 'waddle'.",
            "Penguins have an organ above their eyes that converts seawater to freshwater.",
            "Penguins spend around half of their lives in water and the other half on land.",
            "The smallest penguin species is the Little Blue Penguin, which stands around 16 inches tall."
        ]
        return random.choice(facts)

    def _get_random_motivational_quote(self):
        quotes = [
            "Believe you can and you're halfway there.",
            "Act as if what you do makes a difference. It does.",
            "Success is not final, failure is not fatal: It is the courage to continue that counts.",
            "Never bend your head. Always hold it high. Look the world straight in the eye.",
            "What you get by achieving your goals is not as important as what you become by achieving your goals."
        ]
        return random.choice(quotes)
