"""Module to find the route between two cities using Uniform-Cost and A* Search algorithms.

Functions:
    - parse_road_system
    - parse_heuristic
    - uninformed_search
    - informed_search
"""

import sys

from pathlib import Path
from queue import PriorityQueue
from typing import Final


__all__ = ["informed_search", "parse_heuristic", "parse_road_system", "uninformed_search"]
__author__ = "Gavin Meyer"


def parse_road_system(filename: Path) -> dict[str, dict[str, float]]:
    """Parses the road system data from the given file.

    Args:
        filename: The file containing the road system data.

    Returns:
        dict: A dictionary representing the road connections.
    """
    graph: dict[str, dict[str, float]] = {}
    with Path.open(filename, encoding="locale") as file:
        for line in file:
            if line.strip() == "END OF INPUT":
                break
            parts = line.split()
            city1, city2, distance = parts[0], parts[1], float(parts[2])

            if city1 not in graph:
                graph[city1] = {}
            if city2 not in graph:
                graph[city2] = {}

            # Assuming bi-directional roads
            graph[city1][city2] = distance
            graph[city2][city1] = distance

    return graph


def parse_heuristic(heuristic_file: Path) -> dict[str, float]:
    """Parses the heuristic file and returns a dictionary of heuristic values for each city.

    Args:
        heuristic_file: The file containing the heuristic values.

    Returns:
        dict: A dictionary of heuristic values for each city.
    """
    heuristic = {}
    with Path.open(heuristic_file) as file:
        for line in file:
            if line.strip() == "END OF INPUT":
                break
            parts = line.split()
            city, h_value = parts[0], float(parts[1])
            heuristic[city] = h_value

    return heuristic


def uninformed_search(
    graph: dict[str, dict[str, float]], origin: str, destination: str
) -> tuple[int, int, int, float, list[tuple[str, str, float]] | None]:
    """Performs Uniform-Cost Search in the graph from origin to destination.

    Args:
        graph: A dictionary representing the road connections.
        origin: The starting city.
        destination: The destination city.

    Returns:
        tuple: Tuple containing the number of nodes popped, expanded, generated, distance, and path.
    """
    sys.stdout.write("Uninformed Search\n")
    # Priority Queue to hold (cumulative cost, current city, path)
    frontier: PriorityQueue[tuple[float, str, list[tuple[str, str, float]]]] = PriorityQueue()
    frontier.put((0, origin, []))

    # Set to keep track of explored cities
    explored = set()

    # Variables to track nodes popped, expanded, and generated
    nodes_popped: int = 0
    nodes_expanded: int = 0
    nodes_generated: int = 0

    while not frontier.empty():
        nodes_popped += 1
        current_cost, current_city, path = frontier.get()

        # Check if we have reached the destination
        if current_city == destination:
            return nodes_popped, nodes_expanded, nodes_generated, current_cost, path

        # If the current city has not been explored, add it to the explored set
        if current_city not in explored:
            explored.add(current_city)
            nodes_expanded += 1

            # For each neighbor of the current city, add to the frontier
            for neighbor, distance in graph[current_city].items():
                nodes_generated += 1
                if neighbor not in explored:
                    new_cost = current_cost + distance
                    new_path = [*path, (current_city, neighbor, distance)]
                    frontier.put((new_cost, neighbor, new_path))

    # No path found
    return nodes_popped, nodes_expanded, nodes_generated, float("inf"), None


def informed_search(
    graph: dict[str, dict[str, float]], origin: str, destination: str, heuristic: dict[str, float]
) -> tuple[int, int, int, float, list[tuple[str, str, float]] | None]:
    """Performs A* Search in the graph from origin to destination using the provided heuristic.

    Args:
        graph: A dictionary representing the road connections.
        origin: The starting city.
        destination: The destination city.
        heuristic: A dictionary of heuristic values for each city.

    Returns:
        tuple: Tuple containing the number of nodes popped, expanded, generated, distance, and path.
    """
    sys.stdout.write("Informed Search\n")
    # Priority Queue to hold (estimated total cost, current cost, current city, path)
    frontier: PriorityQueue[tuple[float, float, str, list[tuple[str, str, float]]]] = (
        PriorityQueue()
    )
    frontier.put((heuristic.get(origin, float("inf")), 0, origin, []))

    # Set to keep track of explored cities
    explored = set()

    # Variables to track nodes popped, expanded, and generated
    nodes_popped: int = 0
    nodes_expanded: int = 0
    nodes_generated: int = 0

    while not frontier.empty():
        nodes_popped += 1
        estimated_total, current_cost, current_city, path = frontier.get()

        # Check if we have reached the destination
        if current_city == destination:
            return nodes_popped, nodes_expanded, nodes_generated, current_cost, path

        # If the current city has not been explored, add it to the explored set
        if current_city not in explored:
            explored.add(current_city)
            nodes_expanded += 1

            # For each neighbor of the current city, estimate the total cost & add to the frontier
            for neighbor, distance in graph[current_city].items():
                nodes_generated += 1
                if neighbor not in explored:
                    new_cost = current_cost + distance
                    estimated_total = new_cost + heuristic.get(neighbor, float("inf"))
                    new_path = [*path, (current_city, neighbor, distance)]
                    frontier.put((estimated_total, new_cost, neighbor, new_path))

    # No path found
    return nodes_popped, nodes_expanded, nodes_generated, float("inf"), None


def main() -> None:
    """Main function to find the route based on command line arguments.

    Performs either uninformed or informed search and prints the output.
    """
    max_args: Final[int] = 5

    # Check for valid number of arguments
    if len(sys.argv) not in {4, 5}:
        sys.stdout.write("Invalid number of arguments.\n")
        return

    # Parse command line arguments
    input_filename = sys.argv[1]
    origin_city = sys.argv[2]
    destination_city = sys.argv[3]
    heuristic_filename = sys.argv[4] if len(sys.argv) == max_args else None

    graph = parse_road_system(Path(input_filename))

    # Execute the appropriate search and capture output
    if heuristic_filename:
        heuristic = parse_heuristic(Path(heuristic_filename))
        nodes_popped, nodes_expanded, nodes_generated, distance, path = informed_search(
            graph, origin_city, destination_city, heuristic
        )
    else:
        nodes_popped, nodes_expanded, nodes_generated, distance, path = uninformed_search(
            graph, origin_city, destination_city
        )

    # Print the output
    sys.stdout.write("Nodes Popped: " + str(nodes_popped) + "\n")
    sys.stdout.write("Nodes Expanded: " + str(nodes_expanded) + "\n")
    sys.stdout.write("Nodes Generated: " + str(nodes_generated) + "\n")

    if path is not None:
        sys.stdout.write(f"Distance: {distance:.1f} km\n")
        sys.stdout.write("Route: \n")
        for city1, city2, dist in path:
            sys.stdout.write(f"{city1} to {city2}, {dist:.1f} km\n")
    else:
        sys.stdout.write("Distance: Infinity\n")
        sys.stdout.write("Route:\nNone\n")


if __name__ == "__main__":
    main()
