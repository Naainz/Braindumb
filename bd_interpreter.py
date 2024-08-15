#!/usr/bin/env python3

import sys
import os

# Resolve the actual path even if the script is run via a symlink
script_path = os.path.realpath(__file__)
script_dir = os.path.dirname(script_path)
src_path = os.path.join(script_dir, 'src')

print(f"Adding {src_path} to sys.path")
sys.path.insert(0, src_path)

from interpreter import Interpreter  # Importing the Interpreter class from the src directory

def main():
    if len(sys.argv) != 2:
        print("Usage: bd {path_to_bdpp_file}")
        return

    path = sys.argv[1]
    with open(path, 'r') as file:
        code = file.read()

    interpreter = Interpreter(code)
    interpreter.run()

if __name__ == "__main__":
    main()
