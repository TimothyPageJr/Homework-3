
from pathlib import Path
from testif import testif as professor_testif


# Tests
def testif(testname: str, condition: bool) -> None:
    """Run a Boolean test using the professor's testif function."""
    professor_testif(
        condition,
        testname,
        "Passed",
        "Failed"
    )

# Read
def ed_read(filename: str, from_: int = 0, to: int = -1) -> str:
    """
    Read text from a UTF-8 file.

    Preconditions:
        filename identifies an existing readable file.
        from_ and to are valid integer positions.
        from_ must be nonnegative.
        to must be -1 or at least from_.
        to cannot exceed the file length.

    Postconditions:
        Returns text in the half-open interval [from_, to).
        A value of -1 for to means the end of the file.
        Does not modify the file.

    Raises:
        ValueError for invalid position ranges.
        IndexError if to exceeds the file length.
        File I/O exceptions propagate to the caller.
    """
    if from_ < 0 or (to != -1 and to < from_):
        raise ValueError("Invalid read positions.")

    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()

    if to > len(content):
        raise IndexError("End position exceeds file length.")

    if from_ > len(content):
        raise IndexError("Start position exceeds file length.")

    if to == -1:
        return content[from_:]

    return content[from_:to]


# Find
def ed_find(filename: str, search_str: str) -> list[int]:
    """
    Find all positions where a string occurs in a UTF-8 file.

    Preconditions:
        filename identifies an existing readable file.
        search_str must be a nonempty string.

    Postconditions:
        Returns a list of starting positions of matches.
        Returns an empty list when no matches exist.
        Does not modify the file.

    Raises:
        ValueError if search_str is empty.
        File I/O exceptions propagate to the caller.
    """
    if search_str == "":
        raise ValueError("Search string cannot be empty.")

    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()

    positions = []
    start = 0

    while True:
        index = content.find(search_str, start)

        if index == -1:
            break

        positions.append(index)
        start = index + len(search_str)

    return positions


# Replace
def ed_replace(
    filename: str,
    search_str: str,
    replace_with: str,
    occurrence: int = -1
) -> int:
    """
    Replace text in a UTF-8 file.

    Preconditions:
        filename identifies an existing readable/writable file.
        search_str must be nonempty.
        occurrence must be -1 or a nonnegative integer.

    Postconditions:
        If occurrence is -1, replaces every match.
        Otherwise replaces the zero-based selected match.
        Returns the number of replacements performed.
        Leaves the file unchanged if no replacement is made.

    Raises:
        ValueError for an empty search string or invalid occurrence.
        File I/O exceptions propagate to the caller.
    """
    if search_str == "":
        raise ValueError("Search string cannot be empty.")

    if occurrence < -1:
        raise ValueError("Occurrence must be -1 or greater.")

    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()

    positions = []
    start = 0

    while True:
        index = content.find(search_str, start)

        if index == -1:
            break

        positions.append(index)
        start = index + len(search_str)

    if occurrence == -1:
        count = len(positions)

        if count == 0:
            return 0

        updated = content.replace(search_str, replace_with)

    else:
        if occurrence >= len(positions):
            return 0

        index = positions[occurrence]
        updated = (
            content[:index]
            + replace_with
            + content[index + len(search_str):]
        )
        count = 1

    with open(filename, "w", encoding="utf-8") as file:
        file.write(updated)

    return count


# Append
def ed_append(filename: str, string: str) -> int:
    """
    Append text to the end of a UTF-8 file.

    Preconditions:
        filename is a valid writable file path.
        string is a string.

    Postconditions:
        Creates the file if it does not exist.
        Appends the provided string without removing existing text.
        Returns the number of characters appended.

    Raises:
        File I/O exceptions propagate to the caller.
    """
    with open(filename, "a", encoding="utf-8") as file:
        file.write(string)

    return len(string)


# Test Find
def test_ed_find() -> None:
    """Test finding existing, repeated, and missing strings."""
    filename = "test_find.txt"
    Path(filename).write_text(
        "01234567890123456789", encoding="utf-8"
    )

    testif("Find two matches",
           ed_find(filename, "345") == [3, 13])

    testif("Find missing text",
           ed_find(filename, "356") == [])

    testif("Find first characters",
           ed_find(filename, "012") == [0, 10])

    testif("Find entire text",
           ed_find(filename, "01234567890123456789") == [0])

    Path(filename).unlink()


# Test Replace
def test_ed_replace() -> None:
    """Test replacing one, all, and nonexistent occurrences."""
    filename = "test_replace.txt"
    original = "01234567890123456789"

    Path(filename).write_text(original, encoding="utf-8")

    count = ed_replace(filename, "345", "ABCDE", 1)

    testif("Replace second match count", count == 1)

    testif(
        "Replace second match content",
        ed_read(filename) == "0123456789012ABCDE6789"
    )

    Path(filename).write_text(original, encoding="utf-8")

    count = ed_replace(filename, "345", "ABCDE")

    testif("Replace all count", count == 2)

    testif(
        "Replace all content",
        ed_read(filename) == "012ABCDE6789012ABCDE6789"
    )

    count = ed_replace(filename, "XYZ", "ABC")

    testif("Replace missing text", count == 0)

    count = ed_replace(filename, "ABCDE", "HELLO", 10)

    testif("Replace invalid occurrence", count == 0)

    Path(filename).unlink()


# Main
def main() -> None:
    """Demonstrate the editing functions and run unit tests."""

    print("COP 4045 - Homework 3 - Problem 4")
    print("FAU Student ID: YOUR_ID_HERE")

    filename = "file1.txt"

    # Setup
    Path(filename).write_text("", encoding="utf-8")

    # Append
    print("\nAppend")
    print("Characters written:", ed_append(filename, "0123456789"))
    print("Characters written:", ed_append(filename, "0123456789"))

    # Read
    print("\nRead")
    print("Read positions 3 to 9:", ed_read(filename, 3, 9))
    print("Read from position 3:", ed_read(filename, 3))

    # Find
    print("\nFind")
    print("Find 345:", ed_find(filename, "345"))
    print("Find 356:", ed_find(filename, "356"))

    # Replace
    print("\nReplace")
    print("Replace second occurrence:",
          ed_replace(filename, "345", "ABCDE", 1))
    print("Updated file:", ed_read(filename))

    # Reset
    Path(filename).write_text(
        "01234567890123456789", encoding="utf-8"
    )

    print("Replace all occurrences:",
          ed_replace(filename, "345", "ABCDE"))
    print("Updated file:", ed_read(filename))

    # Tests
    print("\nUnit Tests")
    test_ed_find()
    test_ed_replace()

    print("\nProblem 4 completed.")


# Run
if __name__ == "__main__":
    main()
