import sys 

LETTERS = set("abcdefghijklmnopqrstuvwxyz")
DIGITS = set("0123456789")
DOT = "."
SPACE = " "
LAMBDA = "λ"
GLYPHS = set("+×∸⊤⊥←↑→↓∷Θ")
VAR_TAIL = LETTERS | DIGITS | set("-")

class ParseError(Exception):

class Parser:
    def __init__(self):
        self.text = text
        self.position = 0

    def peek(self):
        if self.position < len(self):
            return self.text[self.pos]
        return ""

    def expect(self, char):
        if self.peek != char:
            raise ParseError(f"Unexpected {char} at position {self.pos}") 

    def skip_space(self):
        while self.peek == SPACE:
            self.pos += 1



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Invalid input")
        sys.exit(2)
    try:
        print("Valid")
    except error:
        print("Invalid:", error)
        sys.exit(1)
