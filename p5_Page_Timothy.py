
"""COP 4045 Homework 3 - Problem 5."""

import sys
import turtle
from testif import testif as professor_testif


# Tests
def testif(name: str, condition: bool) -> None:
    """Run a test using the professor's testif function."""
    professor_testif(condition, name, "Passed", "Failed")


# Leaf
def draw_leaf_straight(level: int, stem_length: float) -> None:
    """Draw a vertical recursive leaf with a straight stem.

    Preconditions: level >= 1 and stem_length > 0.
    Postcondition: A leaf is drawn using turtle graphics.
    """
    if level < 1 or stem_length <= 0:
        raise ValueError("Invalid leaf parameters")

    screen = turtle.Screen()
    screen.setup(900, 850)
    screen.title("Problem 5 - Straight Recursive Leaf")
    screen.bgcolor("white")
    screen.tracer(0)

    pen = turtle.Turtle()
    pen.hideturtle()
    pen.speed(0)
    pen.pensize(2)
    pen.color("forestgreen")

    pen.penup()
    pen.goto(0, -320)
    pen.setheading(90)
    pen.pendown()

    pen.forward(stem_length)

    # Branches
    def branch(depth: int, length: float) -> None:
        """Draw a recursively branching leaf structure."""
        if depth == 0:
            return

        start = pen.position()
        heading = pen.heading()

        pen.pensize(max(1, depth * 0.65))
        pen.forward(length)

        tip = pen.position()

        if depth == 1:
            pen.dot(7, "green")
        else:
            pen.left(38)
            branch(depth - 1, length * 0.72)

            pen.penup()
            pen.goto(tip)
            pen.setheading(heading)
            pen.pendown()

            pen.right(38)
            branch(depth - 1, length * 0.72)

        pen.penup()
        pen.goto(start)
        pen.setheading(heading)
        pen.pendown()

    branch(level, 85)
    screen.update()
    screen.mainloop()


# Curved
def draw_leaf_curved(level: int, stem_length: float) -> None:
    """Draw a curved recursive leaf.

    Preconditions: level >= 1 and stem_length > 0.
    Postcondition: A curved leaf is drawn using turtle graphics.
    """
    if level < 1 or stem_length <= 0:
        raise ValueError("Invalid leaf parameters")

    screen = turtle.Screen()
    screen.setup(900, 850)
    screen.title("Problem 5 - Curved Recursive Leaf")
    screen.bgcolor("white")
    screen.tracer(0)

    pen = turtle.Turtle()
    pen.hideturtle()
    pen.speed(0)
    pen.color("darkgreen")
    pen.pensize(2)

    pen.penup()
    pen.goto(0, -320)
    pen.setheading(90)
    pen.pendown()
    pen.forward(stem_length)

    # Branches
    def branch(depth: int, length: float) -> None:
        """Draw curved recursive branches."""
        if depth == 0:
            return

        start = pen.position()
        heading = pen.heading()

        pen.pensize(max(1, depth * 0.65))

        for _ in range(5):
            pen.forward(length / 5)
            pen.right(3)

        tip = pen.position()
        tip_heading = pen.heading()

        if depth == 1:
            pen.dot(7, "green")
        else:
            pen.left(40)
            branch(depth - 1, length * 0.72)

            pen.penup()
            pen.goto(tip)
            pen.setheading(tip_heading)
            pen.pendown()

            pen.right(35)
            branch(depth - 1, length * 0.72)

        pen.penup()
        pen.goto(start)
        pen.setheading(heading)
        pen.pendown()

    branch(level, 85)
    screen.update()
    screen.mainloop()


# Conversion
def strB(n: int, base: int = 10) -> str:
    """Convert a nonnegative integer to a string in the given base.

    Preconditions: n >= 0 and 2 <= base <= 26.
    Postcondition: Returns the recursive base conversion.
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an integer")

    if not isinstance(base, int) or isinstance(base, bool):
        raise TypeError("base must be an integer")

    if n < 0:
        raise ValueError("n cannot be negative")

    if not 2 <= base <= 26:
        raise ValueError("base must be between 2 and 26")

    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    if n < base:
        return digits[n]

    return strB(n // base, base) + digits[n % base]


# Binomial
def Cnk_m(n: int, k: int) -> int:
    """Calculate n choose k recursively with memoization.

    Preconditions: n and k are integers, 0 <= k <= n.
    Postcondition: Returns the binomial coefficient.
    """
    if not isinstance(n, int) or not isinstance(k, int):
        raise TypeError("n and k must be integers")

    if isinstance(n, bool) or isinstance(k, bool):
        raise TypeError("n and k must be integers")

    if n < 0 or k < 0 or k > n:
        raise ValueError("Require 0 <= k <= n")

    memo: dict[tuple[int, int], int] = {}

    # Recursion
    def calculate(a: int, b: int) -> int:
        """Return a binomial coefficient using cached results."""
        if b == 0 or b == a:
            return 1

        b = min(b, a - b)
        key = (a, b)

        if key in memo:
            return memo[key]

        result = calculate(a - 1, b - 1) + calculate(a - 1, b)
        memo[key] = result
        return result

    return calculate(n, k)


# Pairs
def make_pairs(
    seq1: list,
    seq2: list,
    accumulator: list | None = None
) -> list:
    """Recursively pair matching positions in two lists.

    Preconditions: seq1 and seq2 are lists.
    Postcondition: Returns pairs up to the shorter list length.
    No loops or list comprehensions are used.
    """
    if accumulator is None:
        accumulator = []

    if not seq1 or not seq2:
        return accumulator

    accumulator.append((seq1[0], seq2[0]))

    return make_pairs(seq1[1:], seq2[1:], accumulator)


# Conversion Tests
def test_strB() -> None:
    """Run four tests for recursive base conversion."""
    testif("Binary conversion", strB(42, 2) == "101010")
    testif("Octal conversion", strB(64, 8) == "100")
    testif("Hex conversion", strB(255, 16) == "FF")
    testif("Zero conversion", strB(0, 26) == "0")


# Binomial Tests
def test_Cnk_m() -> None:
    """Run four tests for memoized binomial coefficients."""
    testif("C(5,2)", Cnk_m(5, 2) == 10)
    testif("C(10,3)", Cnk_m(10, 3) == 120)
    testif("C(20,10)", Cnk_m(20, 10) == 184756)
    testif("C(30,0)", Cnk_m(30, 0) == 1)


# Pair Tests
def test_make_pairs() -> None:
    """Run five tests for recursive list pairing."""
    testif(
        "Equal lists",
        make_pairs([10, 20], ["a", "b"]) ==
        [(10, "a"), (20, "b")]
    )

    testif(
        "Shorter second list",
        make_pairs([1, 2, 3], [8]) == [(1, 8)]
    )

    testif(
        "Shorter first list",
        make_pairs([5], [6, 7, 8]) == [(5, 6)]
    )

    testif(
        "Empty first list",
        make_pairs([], [1, 2]) == []
    )

    testif(
        "Empty second list",
        make_pairs([1, 2], []) == []
    )


# Run Cnk
def run_Cnk() -> None:
    """Display selected binomial coefficient calculations."""
    print("\nBinomial Coefficients")
    print("C(8, 3) =", Cnk_m(8, 3))
    print("C(15, 5) =", Cnk_m(15, 5))
    print("C(25, 12) =", Cnk_m(25, 12))
    print("C(40, 20) =", Cnk_m(40, 20))


# Main
def main() -> None:
    """Run tests, demonstrate functions, and draw a leaf."""
    print("COP 4045 - Homework 3 - Problem 5")
    print("FAU Student ID: YOUR_ID_HERE")

    print("\nPart B - Base Conversion")
    print("strB(42, 2) =", strB(42, 2))
    print("strB(255, 16) =", strB(255, 16))
    print("strB(500, 13) =", strB(500, 13))
    print("strB(2026, 26) =", strB(2026, 26))

    print("\nPart C - Memoized Binomial")
    run_Cnk()

    print("\nPart D - Making Pairs")
    print(make_pairs([10, 20, 30], ["A", "B", "C"]))
    print(make_pairs([1, 2, 3, 4], [9, 8]))

    print("\nUnit Tests")
    test_strB()
    test_Cnk_m()
    test_make_pairs()

    print("\nAll 13 tests completed.")
    print("Opening turtle drawing...")

    if len(sys.argv) > 1 and sys.argv[1] == "curved":
        draw_leaf_curved(6, 120)
    else:
        draw_leaf_straight(6, 120)


# Start
if __name__ == "__main__":
    main()
