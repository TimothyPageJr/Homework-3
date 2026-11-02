"""COP 4045 Homework 3, Problem 6: a polymorphic file-system hierarchy."""

from __future__ import annotations

import unittest


class Entry:
    """Base class for a named entry in a file-system hierarchy."""

    def __init__(self, name: str) -> None:
        """Create an entry with a name and no parent folder."""
        if not name:
            raise ValueError("An entry name cannot be empty.")
        self.name: str = name
        self._parent: Folder | None = None

    def parent(self) -> Folder | None:
        """Return this entry's containing folder, or None for a root entry."""
        return self._parent

    def size(self) -> int:
        """Return the entry's size in bytes."""
        raise NotImplementedError("Entry subclasses must implement size().")

    def absolute_path(self) -> list[Entry]:
        """Return this entry followed by its ancestors, ending at the root."""
        if self._parent is None:
            return [self]
        return [self, *self._parent.absolute_path()]


class File(Entry):
    """A file with a nonnegative size measured in bytes."""

    def __init__(self, name: str, bytes_used: int) -> None:
        """Create a file and validate its size."""
        super().__init__(name)
        self.bytes_used = bytes_used

    @property
    def bytes_used(self) -> int:
        """Return the number of bytes used by this file."""
        return self._bytes_used

    @bytes_used.setter
    def bytes_used(self, value: int) -> None:
        """Set the file size, rejecting non-integers and negative values."""
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("bytes_used must be an integer.")
        if value < 0:
            raise ValueError("bytes_used cannot be negative.")
        self._bytes_used: int = value

    def size(self) -> int:
        """Return this file's size in bytes."""
        return self.bytes_used


class Folder(Entry):
    """A folder that contains entries and reports their combined size."""

    def __init__(self, name: str) -> None:
        """Create an empty folder."""
        super().__init__(name)
        self._children: list[Entry] = []

    def add(self, entry: Entry) -> None:
        """Add an entry, preventing cycles and multiple parent folders."""
        if not isinstance(entry, Entry):
            raise TypeError("A folder can contain only Entry instances.")
        if entry is self:
            raise ValueError("A folder cannot contain itself.")
        if entry.parent() is self:
            return
        if entry.parent() is not None:
            raise ValueError("An entry cannot belong to more than one folder.")

        ancestor: Folder | None = self
        while ancestor is not None:
            if ancestor is entry:
                raise ValueError("Adding this entry would create a cycle.")
            ancestor = ancestor.parent()

        entry._parent = self
        self._children.append(entry)

    def children(self) -> tuple[Entry, ...]:
        """Return an immutable tuple of this folder's direct entries."""
        return tuple(self._children)

    def size(self) -> int:
        """Return the combined size of all files in this folder's subtree."""
        return sum(child.size() for child in self._children)


def find_large_files(entry: Entry, minimum_size: int) -> list[File]:
    """Recursively find files at least as large as the inclusive threshold."""
    if isinstance(minimum_size, bool) or not isinstance(minimum_size, int):
        raise TypeError("minimum_size must be an integer.")
    if minimum_size < 0:
        raise ValueError("minimum_size cannot be negative.")

    if isinstance(entry, File):
        return [entry] if entry.size() >= minimum_size else []
    if isinstance(entry, Folder):
        matches: list[File] = []
        for child in entry.children():
            matches.extend(find_large_files(child, minimum_size))
        return matches
    raise TypeError("entry must be a File or Folder.")


def build_sample_hierarchy() -> Folder:
    """Build and return a sample hierarchy with at least three folder levels."""
    root: Folder = Folder("root")
    users: Folder = Folder("Users")
    student: Folder = Folder("Timothy")
    documents: Folder = Folder("Documents")
    course: Folder = Folder("COP4045")
    homework: Folder = Folder("Homework3")

    root.add(users)
    users.add(student)
    student.add(documents)
    documents.add(course)
    course.add(homework)

    homework.add(File("p6_Page_Timothy.py", 12_500))
    homework.add(File("notes.txt", 700))
    course.add(File("syllabus.pdf", 950_000))
    users.add(File("profile.png", 4_200))
    return root


def print_entry_details(entry: Entry) -> None:
    """Print an entry's polymorphic size and path, then its descendants."""
    print(
        f"{type(entry).__name__}: {format_path(entry.absolute_path())} "
        f"({entry.size()} bytes)"
    )
    if isinstance(entry, Folder):
        for child in entry.children():
            print_entry_details(child)


def format_path(path_entries: list[Entry]) -> str:
    """Format an entry-to-root path list as a readable slash-separated path."""
    return "/" + "/".join(entry.name for entry in reversed(path_entries))


class EntryTests(unittest.TestCase):
    """Unit tests for hierarchy paths, sizes, and recursive file searches."""

    def setUp(self) -> None:
        """Build a nested test hierarchy."""
        self.root: Folder = Folder("root")
        self.documents: Folder = Folder("documents")
        self.archive: Folder = Folder("archive")
        self.large_file: File = File("large.bin", 2_000)
        self.medium_file: File = File("medium.bin", 1_000)
        self.small_file: File = File("small.bin", 250)

        self.root.add(self.documents)
        self.documents.add(self.archive)
        self.archive.add(self.large_file)
        self.documents.add(self.medium_file)
        self.root.add(self.small_file)

    def test_absolute_path_is_recursive(self) -> None:
        """Check the exact entry-to-root list and its order."""
        self.assertEqual(self.root.absolute_path(), [self.root])
        self.assertEqual(
            self.large_file.absolute_path(),
            [
                self.large_file,
                self.archive,
                self.documents,
                self.root,
            ],
        )
        self.assertIs(self.large_file.parent(), self.archive)

    def test_children_returns_tuple(self) -> None:
        """Check that direct children are exposed as an immutable tuple."""
        self.assertEqual(self.documents.children(), (self.archive, self.medium_file))
        self.assertIsInstance(self.documents.children(), tuple)

    def test_find_large_files_recurses_and_includes_threshold(self) -> None:
        """Check recursive searches at two thresholds, including equality."""
        self.assertEqual(
            find_large_files(self.root, 1_000),
            [self.large_file, self.medium_file],
        )
        self.assertEqual(find_large_files(self.root, 1_500), [self.large_file])

    def test_folder_size_includes_nested_files(self) -> None:
        """Check that nested file sizes contribute to parent folder totals."""
        self.assertEqual(self.root.size(), 3_250)
        self.assertEqual(self.documents.size(), 3_000)

    def test_file_rejects_negative_size(self) -> None:
        """Check that a file cannot be initialized with a negative size."""
        with self.assertRaises(ValueError):
            File("invalid.bin", -1)


def main() -> None:
    """Demonstrate the hierarchy and run the unit tests."""
    print("COP 4045 - Homework 3 - Problem 6")
    print("FAU Student ID: YOUR_ID_HERE")

    root: Folder = build_sample_hierarchy()
    print("\nPolymorphic sizes and absolute paths:")
    print_entry_details(root)

    print(
        f"\nTotal size of {format_path(root.absolute_path())}: "
        f"{root.size()} bytes"
    )
    for minimum_size in (1_000, 10_000):
        print(f"\nFiles at least {minimum_size} bytes:")
        matches: list[File] = find_large_files(root, minimum_size)
        if matches:
            for file in matches:
                print(
                    f"{format_path(file.absolute_path())} "
                    f"({file.size()} bytes)"
                )
        else:
            print("None")

    print("\nUnit tests:")
    unittest.main(argv=["p6_Page_Timothy.py"], exit=False)


if __name__ == "__main__":
    main()
