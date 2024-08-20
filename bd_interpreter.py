#!/usr/bin/env python3

import sys
import os

script_path = os.path.realpath(__file__)
script_dir = os.path.dirname(script_path)
src_path = os.path.join(script_dir, 'src')

sys.path.insert(0, src_path)

from interpreter import Interpreter

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
