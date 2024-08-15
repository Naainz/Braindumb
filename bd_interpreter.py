#!/usr/bin/env python3

import sys
from src.interpreter import Interpreter

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