
"""COP 4045 - Homework 3 - Problem 2: Parking Permits."""


# ParkingPermit
class ParkingPermit:
    """Represent a university parking permit."""

    # Constructor
    def __init__(
        self,
        owner: str,
        months: int,
        fees: dict[str, float]
    ) -> None:
        """Store the owner, months, and permit fee schedule."""
        if months <= 0:
            raise ValueError("Months must be positive")

        self.owner = owner
        self.months = months
        self.fees = fees.copy()

    # Cost
    def cost(self) -> float:
        """Return the permit cost; subclasses override this."""
        raise NotImplementedError("Use a specific permit type")

    # String
    def __str__(self) -> str:
        """Return a readable description of the permit."""
        return (
            f"Owner: {self.owner}, "
            f"Months: {self.months}"
        )

    # Representation
    def __repr__(self) -> str:
        """Return a detailed representation of the permit."""
        return (
            f"ParkingPermit({self.owner!r}, "
            f"{self.months!r}, {self.fees!r})"
        )


# StudentPermit
class StudentPermit(ParkingPermit):
    """Represent a student parking permit."""

    # Constructor
    def __init__(
        self,
        owner: str,
        months: int,
        fees: dict[str, float],
        vehicles: int
    ) -> None:
        """Initialize a student permit and vehicle count."""
        super().__init__(owner, months, fees)

        if vehicles < 1:
            raise ValueError("At least one vehicle is required")

        self.vehicles = vehicles

    # Cost
    def cost(self) -> float:
        """Calculate monthly fees and extra vehicle fees."""
        monthly = self.fees["student_monthly"]
        extra = self.fees["extra_vehicle"]

        return (
            self.months * monthly
            + max(0, self.vehicles - 1) * extra
        )

    # String
    def __str__(self) -> str:
        """Return student permit information."""
        return (
            f"Student Permit | {super().__str__()}, "
            f"Vehicles: {self.vehicles}, "
            f"Cost: ${self.cost():.2f}"
        )

    # Representation
    def __repr__(self) -> str:
        """Return the student permit representation."""
        return (
            f"StudentPermit({self.owner!r}, "
            f"{self.months!r}, {self.fees!r}, "
            f"{self.vehicles!r})"
        )


# FacultyPermit
class FacultyPermit(ParkingPermit):
    """Represent a faculty parking permit."""

    # Constructor
    def __init__(
        self,
        owner: str,
        months: int,
        fees: dict[str, float],
        garage: bool
    ) -> None:
        """Initialize a faculty permit and garage access."""
        super().__init__(owner, months, fees)
        self.garage = garage

    # Cost
    def cost(self) -> float:
        """Calculate faculty parking and garage fees."""
        monthly = self.fees["faculty_monthly"]
        garage_fee = self.fees["garage_monthly"]

        total = self.months * monthly

        if self.garage:
            total += self.months * garage_fee

        return total

    # String
    def __str__(self) -> str:
        """Return faculty permit information."""
        garage_status = "Yes" if self.garage else "No"

        return (
            f"Faculty Permit | {super().__str__()}, "
            f"Garage: {garage_status}, "
            f"Cost: ${self.cost():.2f}"
        )

    # Representation
    def __repr__(self) -> str:
        """Return the faculty permit representation."""
        return (
            f"FacultyPermit({self.owner!r}, "
            f"{self.months!r}, {self.fees!r}, "
            f"{self.garage!r})"
        )


# Summary
def summarize_list(permits: list[ParkingPermit]) -> float:
    """Print each permit owner and cost, then return revenue."""
    total = 0.0

    for permit in permits:
        print(f"{permit.owner}: ${permit.cost():.2f}")
        total += permit.cost()

    return total


# Tests
def main() -> None:
    """Demonstrate the parking permit classes and calculations."""

    print("COP 4045 - Homework 3 - Problem 2")
    print("FAU Student ID: YOUR_ID_HERE")

    # Fees
    fees = {
        "student_monthly": 25.0,
        "extra_vehicle": 10.0,
        "faculty_monthly": 40.0,
        "garage_monthly": 15.0
    }

    # Students
    student1 = StudentPermit("Alex", 4, fees, 2)
    student2 = StudentPermit("Jordan", 3, fees, 1)

    # Faculty
    faculty1 = FacultyPermit("Taylor", 4, fees, True)
    faculty2 = FacultyPermit("Morgan", 2, fees, False)

    # Objects
    print("\nPermit Objects")
    print(student1)
    print(student2)
    print(faculty1)
    print(faculty2)

    # Representation
    print("\nRepresentations")
    print(repr(student1))
    print(repr(faculty1))

    # Summary
    permits: list[ParkingPermit] = [
        student1,
        student2,
        faculty1,
        faculty2
    ]

    print("\nPermit Summary")
    revenue = summarize_list(permits)

    print(f"\nTotal Revenue: ${revenue:.2f}")


# Run
if __name__ == "__main__":
    main()
