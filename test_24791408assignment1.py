import subprocess
import sys

import assignment1_24791408 as mod


def parses(text):
    """True if the parser accepts the text, False if it rejects it."""
    try:
        mod.Parser(text).parse_input()
        return True
    except mod.ParseError:
        return False


fails = []

def check(ok, message):
    print("PASS:" if ok else "FAIL:", message)
    if not ok:
        fails.append(message)


# strings the parser SHOULD accept
valid = [
    "0",
    "42",
    "a",
    "foo",
    "b1-c",
    "+",
    "⊤",
    "λd.d",
    "λ e . e",
    "λf.λg.f",
    "(h k)",
    "(λm.m 5)",
    "((n p) q)",
    "  r  ",
    "λh.(h 1)",
    "(λs.s λt.t)",
    "((a b) (c d))",
    "(a  b)",   # extra spaces between the two parts are fine
    "a-",       # dash allowed inside/at the end of a variable
    "←",
    "007",
    "×",        # every glyph is a valid expression on its own
    "∸",
    "⊥",
    "↑",
    "→",
    "↓",
    "∷",
    "Θ",
]

# strings the parser SHOULD reject
invalid = [
    "",
    "S",
    "1t",
    "-u",
    "(v)",
    "(w z",
    "a b",
    "λc c",
    "λ.d",
    "λ1.e",
    "(1a)",     # no space between the two parts — these three are the only
    "(+5)",     # cases that catch a parser whose mandatory-space check
    "(x+)",     # (expect(SPACE) in parse_application) is broken
    "(vw)",     # rejected too, but for a different reason: "vw" reads as ONE variable
    "()",
    "λa.",      # missing body
    "(a )",     # space but no second part
    "a\n",      # trailing newline — skip_space only skips U+0020, not other whitespace
    "\ta",      # leading tab — same reason
    "λ-.e",     # bound name can't start with a dash
    "λ×.×",     # bound name must be a variable, glyphs don't count
]

for text in valid:
    check(parses(text), repr(text) + " should be accepted")

for text in invalid:
    check(not parses(text), repr(text) + " should be rejected")


# --- exit-code checks: the spec grades these ---
# 0 = valid expression, 1 = invalid expression, 2 = wrong number of arguments

def exit_code(arguments):
    """Run the parser script with the given arguments and give back its exit code."""
    command = [sys.executable, mod.__file__] + arguments
    return subprocess.run(command, capture_output=True).returncode

exit_checks = [
    (["(λk.k 9)"], 0),
    (["⊥"], 0),
    (["(3z)"], 1),         # missing space, rejected at the command line too
    (["λq q"], 1),         # missing dot
    ([], 2),               # no argument at all
    (["p", "q", "r"], 2),  # too many arguments
]

for arguments, wanted in exit_checks:
    code = exit_code(arguments)
    check(code == wanted, f"script with {arguments} exited {code}, wanted {wanted}")


print()
if fails:
    print(len(fails), "test(s) failed")
else:
    print("All tests passed!")
