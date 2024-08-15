from ..src.lexer import Lexer

def test_lexer():
    code = "red x = 3 !!!! print! 'Hello, World!?'"
    lexer = Lexer(code)
    tokens = lexer.tokenize()

    for token in tokens:
        print(token)

if __name__ == "__main__":
    test_lexer()
