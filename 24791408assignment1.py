import sys 

LETTERS = set("abcdefghijklmnopqrstuvwxyz")
DIGITS = set("0123456789")
DOT = "."
SPACE = " "
LAMBDA = "λ"
GLYPHS = set("+×∸⊤⊥←↑→↓∷Θ")
VAR_TAIL = LETTERS | DIGITS | set("-")

class ParseError(Exception):
    pass

class Parser:
    def __init__(self, text):
        self.text = text
        self.position = 0

    def peek(self):
        if self.position < len(self.text):
            return self.text[self.position]
        return ""

    def describe(self):
        char = self.peek()
        return repr(char) if char else "end of input"

    def expect(self, char):
        if self.peek() != char:
            raise ParseError(
                f"expected {char!r} but found {self.describe()} at position {self.position}")
        self.position += 1

    def skip_space(self):
        while self.peek() == SPACE:
            self.position += 1

#1 method per grammer rule 
    def parse_input(self):
        self.skip_space()
        self.parse_expression()
        self.skip_space()

        if self.position != len(self.text):
            raise ParseError(f"Unexpected {self.describe()} at position {self.position}")


    def parse_expression(self):
        char = self.peek()
        if char in DIGITS:
            self.parse_numeral()
        elif char in LETTERS:
            self.parse_variable()
        elif char in GLYPHS:
            self.parse_glyph()
        elif char == LAMBDA:
            self.parse_abstraction()
        elif char == "(":
            self.parse_application()
        else:
            raise ParseError(f"unexpected {self.describe()} at position {self.position}")

    def parse_numeral(self):
        if self.peek() not in DIGITS:
            raise ParseError(f"unexpected {self.describe()} at position {self.position}")

        self.position += 1
        while self.peek() in DIGITS:
            self.position += 1

    def parse_variable(self):
        if self.peek() not in LETTERS:
            raise ParseError(f"unexpected {self.describe()} at position {self.position}")
        self.position += 1
        while self.peek() in VAR_TAIL:
            self.position += 1

    def parse_glyph(self):
        if self.peek() not  in GLYPHS:
            raise ParseError(f"unexpected {self.describe()} at position {self.position}")
        self.position += 1

    def parse_abstraction(self):
        self.expect(LAMBDA)
        self.skip_space()
        self.parse_variable()
        self.skip_space()
        self.expect(DOT)
        self.skip_space()
        self.parse_expression()

    def parse_application(self):
        self.expect("(")
        self.skip_space()
        self.parse_expression()
        self.expect(SPACE)
        self.skip_space()
        self.parse_expression()
        self.skip_space()
        self.expect(")")



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Invalid input")
        sys.exit(2)
    try:
        parser = Parser(sys.argv[1])
        parser.parse_input()
    except ParseError as error: 
        print("Invalid:", error)
        sys.exit(1)
