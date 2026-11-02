
"""COP 4045 - Homework 3 - Problem 3: Predator-Prey-Human Simulation."""

import random
import matplotlib.pyplot as plt


# Island
class Island:
    """Represent an island containing prey, predators, and humans."""

    # Constructor
    def __init__(
        self,
        n: int,
        prey_count: int = 0,
        predator_count: int = 0,
        count_humans: int = 0
    ) -> None:
        """Create an n by n island and populate it with animals."""
        if n <= 0:
            raise ValueError("Island size must be positive")
        if min(prey_count, predator_count, count_humans) < 0:
            raise ValueError("Population counts cannot be negative")
        if prey_count + predator_count + count_humans > n * n:
            raise ValueError("Too many animals for the island")

        self.grid_size = n
        self.grid = [[0 for _ in range(n)] for _ in range(n)]
        self.init_animals(prey_count, predator_count, count_humans)

    # Animals
    def init_animals(
        self,
        prey_count: int,
        predator_count: int,
        count_humans: int
    ) -> None:
        """Place the requested populations in random empty cells."""
        for animal_class, count in (
            (Prey, prey_count),
            (Predator, predator_count),
            (Human, count_humans)
        ):
            placed = 0
            while placed < count:
                x = random.randint(0, self.grid_size - 1)
                y = random.randint(0, self.grid_size - 1)

                if not self.animal(x, y):
                    self.register(animal_class(self, x, y))
                    placed += 1

    # Flags
    def clear_all_moved_flags(self) -> None:
        """Allow each animal to move again during the next tick."""
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                animal = self.grid[x][y]
                if animal:
                    animal.clear_moved_flag()

    # Size
    def size(self) -> int:
        """Return the width of the island grid."""
        return self.grid_size

    # Register
    def register(self, animal: "Animal") -> None:
        """Place an animal at its coordinates."""
        self.grid[animal.x][animal.y] = animal

    # Remove
    def remove(self, animal: "Animal") -> None:
        """Remove an animal if it still occupies its cell."""
        if self.animal(animal.x, animal.y) is animal:
            self.grid[animal.x][animal.y] = 0

    # Location
    def animal(self, x: int, y: int) -> "Animal | int":
        """Return the cell occupant or -1 for an invalid position."""
        if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
            return self.grid[x][y]
        return -1

    # String
    def __str__(self) -> str:
        """Return a printable grid with its origin at the bottom left."""
        lines = []
        for y in range(self.grid_size - 1, -1, -1):
            row = []
            for x in range(self.grid_size):
                animal = self.grid[x][y]
                row.append(str(animal) if animal else ".")
            lines.append("  ".join(row))
        return "\n".join(lines)

    # Prey
    def count_prey(self) -> int:
        """Return the number of living prey."""
        return sum(
            isinstance(self.grid[x][y], Prey)
            for x in range(self.grid_size)
            for y in range(self.grid_size)
        )

    # Predators
    def count_predators(self) -> int:
        """Return the number of living predators."""
        return sum(
            isinstance(self.grid[x][y], Predator)
            for x in range(self.grid_size)
            for y in range(self.grid_size)
        )

    # Humans
    def count_humans(self) -> int:
        """Return the number of living humans."""
        return sum(
            isinstance(self.grid[x][y], Human)
            for x in range(self.grid_size)
            for y in range(self.grid_size)
        )


# Animal
class Animal:
    """Provide common movement and breeding behavior."""

    # Constructor
    def __init__(
        self,
        island: Island,
        x: int = 0,
        y: int = 0,
        s: str = "A"
    ) -> None:
        """Store the animal's island, position, and display symbol."""
        self.island = island
        self.name = s
        self.x = x
        self.y = y
        self.moved = False

    # Position
    def position(self) -> tuple[int, int]:
        """Return the animal's coordinates."""
        return self.x, self.y

    # String
    def __str__(self) -> str:
        """Return the animal's grid symbol."""
        return self.name

    # Search
    def check_grid(
        self,
        type_looking_for: type = int
    ) -> tuple[int, int] | int:
        """Find a neighboring cell of the specified exact type."""
        offsets = [
            (-1, 1), (0, 1), (1, 1),
            (-1, 0), (1, 0),
            (-1, -1), (0, -1), (1, -1)
        ]

        for dx, dy in offsets:
            x = self.x + dx
            y = self.y + dy

            if not (0 <= x < self.island.size()):
                continue
            if not (0 <= y < self.island.size()):
                continue

            if type(self.island.animal(x, y)) is type_looking_for:
                return x, y

        return 0

    # Movement
    def move(self) -> None:
        """Move to an empty neighboring cell if possible."""
        if self.moved:
            return

        location = self.check_grid(int)
        if location:
            self.island.remove(self)
            self.x, self.y = location
            self.island.register(self)
            self.moved = True

    # Breeding
    def breed(self) -> None:
        """Create a new animal of the same class when ready."""
        if self.breed_clock > 0:
            return

        location = self.check_grid(int)
        if location:
            self.breed_clock = self.breed_time
            new_animal = self.__class__(
                self.island, x=location[0], y=location[1]
            )
            self.island.register(new_animal)

    # Flags
    def clear_moved_flag(self) -> None:
        """Reset the movement flag."""
        self.moved = False


# Prey
class Prey(Animal):
    """Represent prey that move and reproduce."""

    breed_time: int = 3

    # Constructor
    def __init__(
        self,
        island: Island,
        x: int = 0,
        y: int = 0,
        s: str = "O"
    ) -> None:
        """Create prey and initialize its breeding clock."""
        super().__init__(island, x, y, s)
        self.breed_clock = self.breed_time

    # Clock
    def clock_tick(self) -> None:
        """Decrease the prey's breeding clock."""
        self.breed_clock -= 1


# Predator
class Predator(Animal):
    """Represent a predator that eats prey and may starve."""

    breed_time: int = 6
    starve_time: int = 3

    # Constructor
    def __init__(
        self,
        island: Island,
        x: int = 0,
        y: int = 0,
        s: str = "X"
    ) -> None:
        """Create a predator with breeding and starvation clocks."""
        super().__init__(island, x, y, s)
        self.breed_clock = self.breed_time
        self.starve_clock = self.starve_time

    # Eating
    def eat(self) -> None:
        """Eat neighboring prey and reset the starvation clock."""
        if self.moved:
            return

        location = self.check_grid(Prey)
        if location:
            prey = self.island.animal(*location)
            self.island.remove(prey)
            self.island.remove(self)
            self.x, self.y = location
            self.island.register(self)
            self.starve_clock = self.starve_time
            self.moved = True

    # Clock
    def clock_tick(self) -> None:
        """Update clocks and remove a starving predator."""
        self.breed_clock -= 1
        self.starve_clock -= 1

        if self.starve_clock <= 0:
            self.island.remove(self)


# Human
class Human(Animal):
    """Represent a human that hunts predators, breeds, and may starve."""

    hunt_time: int = 2
    starve_time: int = 8
    breed_time: int = 12

    # Constructor
    def __init__(
        self,
        island: Island,
        x: int = 0,
        y: int = 0,
        s: str = "H"
    ) -> None:
        """Create a human with hunting, breeding, and starvation clocks."""
        super().__init__(island, x, y, s)
        self.breed_clock = self.breed_time
        self.starve_clock = self.starve_time
        self.hunt_clock = self.hunt_time

    # Hunting
    def hunt(self) -> None:
        """Attempt to kill a neighboring predator when hunting is due."""
        if self.moved or self.hunt_clock > 0:
            return

        location = self.check_grid(Predator)

        if location:
            predator = self.island.animal(*location)
            self.island.remove(predator)
            self.island.remove(self)
            self.x, self.y = location
            self.island.register(self)
            self.starve_clock = self.starve_time
            self.moved = True

        self.hunt_clock = self.hunt_time

    # Clock
    def clock_tick(self) -> None:
        """Decrease all clocks and remove a starving human."""
        self.breed_clock -= 1
        self.starve_clock -= 1
        self.hunt_clock -= 1

        if self.starve_clock <= 0:
            self.island.remove(self)


# Simulation
def main(
    predator_breed_time: int = 6,
    predator_starve_time: int = 3,
    initial_predators: int = 10,
    prey_breed_time: int = 3,
    initial_prey: int = 50,
    size: int = 10,
    ticks: int = 1000,
    human_hunt_time: int = 2,
    human_starve_time: int = 8,
    human_breed_time: int = 12,
    initial_humans: int = 5
) -> None:
    """Simulate three populations and graph their changes over time."""

    # Settings
    Predator.breed_time = predator_breed_time
    Predator.starve_time = predator_starve_time
    Prey.breed_time = prey_breed_time
    Human.hunt_time = human_hunt_time
    Human.starve_time = human_starve_time
    Human.breed_time = human_breed_time

    # Island
    island = Island(
        size, initial_prey, initial_predators, initial_humans
    )

    print("COP 4045 - Homework 3 - Problem 3")
    print("FAU Student ID: YOUR_ID_HERE")

    print("\nStarting Island")
    print(island)

    # Populations
    prey_list: list[int] = [island.count_prey()]
    predator_list: list[int] = [island.count_predators()]
    human_list: list[int] = [island.count_humans()]

    # Ticks
    max_ticks = min(ticks, 1000)

    for tick in range(1, max_ticks + 1):
        island.clear_all_moved_flags()

        for x in range(size):
            for y in range(size):
                animal = island.animal(x, y)

                if not animal:
                    continue

                if isinstance(animal, Human):
                    animal.hunt()
                elif isinstance(animal, Predator):
                    animal.eat()

                if island.animal(animal.x, animal.y) is not animal:
                    continue

                animal.move()
                animal.breed()
                animal.clock_tick()

        prey_list.append(island.count_prey())
        predator_list.append(island.count_predators())
        human_list.append(island.count_humans())

        if tick == 1 or tick % 10 == 0:
            print(
                f"Tick {tick}: "
                f"Prey={prey_list[-1]}, "
                f"Predators={predator_list[-1]}, "
                f"Humans={human_list[-1]}"
            )

        # Convergence
        if len(prey_list) >= 21:
            stable = all(
                len(set(values[-20:])) == 1
                for values in (
                    prey_list, predator_list, human_list
                )
            )
            if stable:
                print(f"Populations converged at tick {tick}.")
                break

    # Results
    print("\nEnding Island")
    print(island)

    print(
        f"Final populations: "
        f"Prey={prey_list[-1]}, "
        f"Predators={predator_list[-1]}, "
        f"Humans={human_list[-1]}"
    )

    # Graph
    plt.plot(prey_list, label="Prey")
    plt.plot(predator_list, label="Predators")
    plt.plot(human_list, label="Humans")

    plt.xlabel("Clock ticks")
    plt.ylabel("Population")
    plt.title("Island Population Simulation")
    plt.legend()
    plt.tight_layout()
    plt.savefig("p3_populations.png")
    plt.show()


# Run
if __name__ == "__main__":
    main()
