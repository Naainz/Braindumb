# Braindumb ++ Deluxe Edition

Braindumb is an esoteric programming language that is built on the foundations of productivity. 

### What does Braindumb mean?

Braindumb is an alternative name of the well-known programming language [Brainfuck](https://en.wikipedia.org/wiki/Brainfuck). The word 'Braindumb' is a portmanteau of the words '**Brain**', and '**Dumb**'.

> - **Brain** - a complex organ in the skull that controls the nervous system, processes information, and enables thought, memory, and emotion

> - **Dumb** - unable to speak, often used to describe someone who is perceived as lacking intelligence or common sense.

## Installation

1. Clone the Repository
```bash
git clone https://github.com/Naainz/Braindumb
cd Braindumb
```

2. Installing prerequisites
```bash
pip install -r src/requirements.txt
```

3. Creating a symlink
```bash
chmod +x bd_interpreter.py
ln -s $(pwd)/bd_interpreter.py /usr/local/bin/bd
```

4. Run `.bdpp` files with the command: `bd {path-to-bdpp-file.bdpp}`

## Features

### Basic Syntax
- **Variable Assignment**: Standard variable assignment using `=`.
- **Mathematical Operations**: Supports addition `+`, subtraction `-`, multiplication `*`, and division `/`.
- **Arrays**: Arrays start at index `-2` and increment by 2. Access array elements using the syntax `my_array at position X`.

### Special Variables

- **Red Variables**: Variables declared with the `red` keyword can only hold odd numbers. If assigned an even number, the value is automatically incremented by 1.
- **Green Variables**: Variables declared with the `green` keyword can only hold even numbers. If assigned an odd number, the value is automatically decremented by 1.
- **Blue Variables**: Variables declared with the `blue` keyword can only hold strings that contain at least one vowel. If no vowel is found, the string is punished by appending "balls" to it.

### Special Syntax

- **`i am inevitable`**: Removes a value from existence in the program. The value is no longer recognized or processed in any output.
- **`and i am ironman`**: Restores a previously removed value so it can be used again. Use `and i am ironman *` to restore all values.
- **Non-Deterministic Operations**: Use the `?` operator for a randomly chosen operation between two numbers.

### Magical Numbers

- **42**: Automatically returns "The answer to life, the universe, and everything."
- **0**: Inverts the sign of the nearest non-zero variable.
- **7**: Randomly changes into any prime number below 100.

### Emoji-Based Logic

- **💩**: When placed before a variable name, it multiplies the variable by 2 if its value is divisible by 3.

### Error and Warning Handling

- **Penguin Facts**: Errors include a random penguin fact.
- **Motivational Quotes**: Warnings are replaced with motivational quotes.
- **Palindrome Variables**: If a variable name is a palindrome, all warnings and errors are displayed in reverse.

### Number Handling

- **Large Numbers**: Numbers greater than 999 must be spelled out (e.g., `1001` should be written as `one thousand one`).

## Example Usage

```plaintext
💩
y = 9
!print! y

my_array = [1, 2, 3, 4, 5]
my_array_value = my_array at position 2
!print! my_array_value

green num = 3
!print! num

i am inevitable 'balls'
text = "bcdfghjklmnpqrstvwxyz"
!print! text
```

## License

This project was licensed under the [MIT License](LICENSE).