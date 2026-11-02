
"""COP 4045 - Homework 3 - Problem 1: NVector."""

from numbers import Real
from testif import testif


class NVector:
    """Represent an N-dimensional vector of real numbers."""

    # Constructor
    def __init__(
        self,
        *values: Real | list[Real] | tuple[Real, ...]
    ) -> None:
        """Initialize the vector with real numbers."""
        if len(values) == 1:
            if not isinstance(values[0], (list, tuple)):
                raise TypeError("A single argument must be a list or tuple")
            self.elements = list(values[0])
        else:
            self.elements = list(values)

        if not all(isinstance(x, Real) for x in self.elements):
            raise TypeError("Vector elements must be real numbers")

    # Length
    def __len__(self) -> int:
        """Return the number of elements."""
        return len(self.elements)

    # Indexing
    def __getitem__(self, index: int) -> Real:
        """Return an element at the specified index."""
        return self.elements[index]

    # Assignment
    def __setitem__(self, index: int, value: Real) -> None:
        """Change an element at the specified index."""
        if not isinstance(value, Real):
            raise TypeError("Value must be a real number")
        self.elements[index] = value

    # String
    def __str__(self) -> str:
        """Return the vector as a string."""
        return str(self.elements)

    # Comparison
    def __eq__(self, other: object) -> bool:
        """Check whether two vectors are equal."""
        if not isinstance(other, NVector):
            return False
        return self.elements == other.elements

    def __ne__(self, other: object) -> bool:
        """Check whether two vectors are different."""
        return not self.__eq__(other)

    # Addition
    def __add__(self, other: object) -> "NVector":
        """Add another vector or a scalar."""
        if isinstance(other, NVector):
            if len(self) != len(other):
                raise ValueError("Vector dimensions must match")
            return NVector([
                self[i] + other[i]
                for i in range(len(self))
            ])

        if isinstance(other, Real):
            return NVector([
                x + other for x in self.elements
            ])

        return NotImplemented

    def __radd__(self, other: object) -> "NVector":
        """Support addition with a scalar on the left."""
        return self.__add__(other)

    # Multiplication
    def __mul__(self, other: object) -> Real:
        """Calculate the sum of element products."""
        if isinstance(other, NVector):
            if len(self) != len(other):
                raise ValueError("Vector dimensions must match")
            return sum(
                self[i] * other[i]
                for i in range(len(self))
            )

        if isinstance(other, Real):
            return sum(x * other for x in self.elements)

        return NotImplemented

    def __rmul__(self, other: object) -> Real:
        """Support multiplication with a scalar on the left."""
        return self.__mul__(other)

    # Zeros
    @classmethod
    def zeros(cls, n: int) -> "NVector":
        """Create a vector containing n zeros."""
        if not isinstance(n, int):
            raise TypeError("Dimension must be an integer")
        if n < 0:
            raise ValueError("Dimension cannot be negative")
        return cls([0] * n)


# Tests
def main() -> None:
    """Test the NVector methods."""

    # Constructor
    v1 = NVector(3, 0, 1, -1)
    v2 = NVector([3, 0, 1, -1])
    v3 = NVector((3, 0, 1, -1))
    v4 = NVector(1, 2, 3, 4)

    testif(v1 == v2, "A1: Multiple arguments", "Works", "Failed")
    testif(v2 == v3, "A2: List and tuple", "Works", "Failed")

    # Length
    testif(len(v1) == 4, "B: Vector length", "Works", "Failed")

    # Indexing
    testif(v1[1] == 0, "C1: Positive indexing", "Works", "Failed")
    testif(v1[-2] == 1, "C2: Negative indexing", "Works", "Failed")

    # Assignment
    v1[2] = 5
    testif(v1[2] == 5, "D: Indexed assignment", "Works", "Failed")

    # String
    testif(
        str(v2) == "[3, 0, 1, -1]",
        "E: String representation", "Works", "Failed"
    )

    # Comparison
    testif(v2 == v3, "F1: Equality", "Works", "Failed")
    testif(v1 != v2, "F2: Inequality", "Works", "Failed")
    testif(
        v2 != [3, 0, 1, -1],
        "F3: Different object type", "Works", "Failed"
    )

    # Addition
    testif(
        v2 + v4 == NVector(4, 2, 4, 3),
        "G1: Vector addition", "Works", "Failed"
    )
    testif(
        v2 + 10 == NVector(13, 10, 11, 9),
        "G2: Scalar addition", "Works", "Failed"
    )
    testif(
        10 + v2 == NVector(13, 10, 11, 9),
        "G3: Reflected addition", "Works", "Failed"
    )

    # Multiplication
    testif(v2 * v4 == 2, "H1: Dot product", "Works", "Failed")
    testif(v2 * 2 == 6, "H2: Scalar multiplication", "Works", "Failed")
    testif(2 * v2 == 6, "H3: Reflected multiplication", "Works", "Failed")

    # Zeros
    testif(
        NVector.zeros(4) == NVector(0, 0, 0, 0),
        "I: Zero vector", "Works", "Failed"
    )

    # Copy
    original = [3, 0, 1, -1]
    copied = NVector(original)
    original[0] = 99
    testif(copied[0] == 3, "Copy independence", "Works", "Failed")

    # Exceptions
    try:
        v2[100]
        index_error = False
    except IndexError:
        index_error = True

    testif(index_error, "Invalid index exception", "Works", "Failed")

    try:
        v2 + NVector(1, 2)
        dimension_error = False
    except ValueError:
        dimension_error = True

    testif(
        dimension_error,
        "Addition dimension exception", "Works", "Failed"
    )

    try:
        v2 * NVector(1, 2)
        dimension_error = False
    except ValueError:
        dimension_error = True

    testif(
        dimension_error,
        "Multiplication dimension exception", "Works", "Failed"
    )


# Run
if __name__ == "__main__":
    main()
    print("FAU Student ID: 23671440")
    print("COP 4045 - Homework 3 - Problem 1")