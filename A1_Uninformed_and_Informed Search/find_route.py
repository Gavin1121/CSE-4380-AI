import sys

from pathlib import Path
from queue import PriorityQueue


# Step 1: Parsing Input Data
def parse_road_system(filename: Path) -> dict:
    """Parses the road system data from the given file.

    Returns a graph representing the road connections.
    """
    graph = {}
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

            graph[city1][city2] = distance
            graph[city2][city1] = distance  # Assuming bidirectional roads

    return graph


def parse_heuristic(heuristic_file: Path) -> dict[str, float]:
    """Parses the heuristic file and returns a dictionary of heuristic values for each city."""
    heuristic = {}
    with Path.open(heuristic_file) as file:
        for line in file:
            if line.strip() == "END OF INPUT":
                break
            parts = line.split()
            city, h_value = parts[0], float(parts[1])
            heuristic[city] = h_value

    return heuristic


# Implementing Uninformed Search (Uniform-Cost Search)
def uninformed_search(graph: dict, origin: str, destination: str):
    """Performs an uninformed search (Uniform-Cost Search) in the graph from origin to destination.

    Returns the path found along with the total distance, nodes popped, expanded, and generated.
    """
    # Priority Queue to hold (cumulative_cost, current_city, path_so_far)
    frontier = PriorityQueue()
    frontier.put((0, origin, []))

    # Set to keep track of explored cities
    explored = set()

    # Variables to track nodes popped, expanded, and generated
    nodes_popped, nodes_expanded, nodes_generated = 0, 0, 0

    while not frontier.empty():
        nodes_popped += 1
        current_cost, current_city, path = frontier.get()

        # Check if we have reached the destination
        if current_city == destination:
            return nodes_popped, nodes_expanded, nodes_generated, current_cost, path

        if current_city not in explored:
            explored.add(current_city)
            nodes_expanded += 1

            for neighbor, distance in graph[current_city].items():
                if neighbor not in explored:
                    new_cost = current_cost + distance
                    new_path = [*path, (current_city, neighbor, distance)]
                    frontier.put((new_cost, neighbor, new_path))
                    nodes_generated += 1

    return nodes_popped, nodes_expanded, nodes_generated, float("inf"), None  # No path found


# Implementing Informed Search (A* Search)
def informed_search(graph: dict, origin: str, destination: str, heuristic: dict[str, float]):
    """Performs an informed search (A* Search) in the graph from origin to destination using the provided heuristic.

    Returns the path found along with the total distance, nodes popped, expanded, and generated.
    """
    # Priority Queue to hold (estimated_total_cost, current_cost, current_city, path_so_far)
    frontier = PriorityQueue()
    frontier.put((heuristic.get(origin, float("inf")), 0, origin, []))

    # Set to keep track of explored cities
    explored = set()

    # Variables to track nodes popped, expanded, and generated
    nodes_popped, nodes_expanded, nodes_generated = 0, 0, 0

    while not frontier.empty():
        nodes_popped += 1
        estimated_total, current_cost, current_city, path = frontier.get()

        # Check if we have reached the destination
        if current_city == destination:
            return nodes_popped, nodes_expanded, nodes_generated, current_cost, path

        if current_city not in explored:
            explored.add(current_city)
            nodes_expanded += 1

            for neighbor, distance in graph[current_city].items():
                if neighbor not in explored:
                    new_cost = current_cost + distance
                    estimated_total = new_cost + heuristic.get(neighbor, float("inf"))
                    new_path = [*path, (current_city, neighbor, distance)]
                    frontier.put((estimated_total, new_cost, neighbor, new_path))
                    nodes_generated += 1

    return nodes_popped, nodes_expanded, nodes_generated, float("inf"), None  # No path found


# function to integrate search algorithms and format the output
def find_route() -> None:
    """Main function to find the route based on command line arguments.

    Performs either uninformed or informed search and prints the output.
    """
    if len(sys.argv) not in {4, 5}:
        print("Invalid number of arguments.")
        return

    input_filename = sys.argv[1]
    origin_city = sys.argv[2]
    destination_city = sys.argv[3]
    heuristic_filename = sys.argv[4] if len(sys.argv) == 5 else None

    # Parse the road system from the input file
    graph = parse_road_system(input_filename)

    # Execute the appropriate search and capture the output
    if heuristic_filename:
        heuristic = parse_heuristic(heuristic_filename)
        nodes_popped, nodes_expanded, nodes_generated, distance, path = informed_search(
            graph, origin_city, destination_city, heuristic
        )
    else:
        nodes_popped, nodes_expanded, nodes_generated, distance, path = uninformed_search(
            graph, origin_city, destination_city
        )

    # Formatting and printing the output
    print("Nodes Popped:", nodes_popped)
    print("Nodes Expanded:", nodes_expanded)
    print("Nodes Generated:", nodes_generated)

    if path is not None:
        print(f"Distance: {distance:.1f} km")
        print("Route:")
        for city1, city2, dist in path:
            print(f"{city1} to {city2}, {dist:.1f} km")
    else:
        print("Distance: infinity")
        print("Route:\nNone")


def main() -> None:
    find_route()


if __name__ == "__main__":
    main()
