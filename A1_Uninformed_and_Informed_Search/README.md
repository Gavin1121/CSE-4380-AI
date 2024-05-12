# Assignment 1 - Uninformed Search and Informed Search

![alt text](../figures/input1_graphic.gif)

## Programming Language

- Python 3.12.1

## Code Structure

- The python script named *find_route.py* contains the main code for the assignment.
- This script contains the main function *main()* which is the entry point for the program.

- The script also contains the following functions:
  - **parse_road_system**
    - This function takes a file path as input and returns a dictionary containing the road system.

  - **parse_heuristic**
    - This function takes a file path as input and returns a dictionary containing the heuristic values.

  - **uninformed_search**
    - This function takes a graph, origin, and destination as input and returns a tuple containing the number of nodes popped, expanded, generated, distance of the solution, and the path of the solution.

  - **informed_search**
    - This function takes a graph, origin, destination, and heuristic as input and returns a tuple containing the number of nodes popped, expanded, generated, distance of the solution, and the path of the solution.

## Running the Script

First, ensure that you have Python 3.12.1 or a compatible python version installed on your machine.
*If not, please refer to the [Python Documentation](https://www.python.org/doc/)*

To run the script, open a terminal and navigate to the directory containing the *find_route.py* file.

**Running Without Heuristic:**

Type the following command in the terminal:

```bash
python find_route.py <input_file/filepath> <origin> <destination>
```

*Note: Replace `<input_file/filepath>`, `<origin>`, and `<destination>` with the appropriate values.*

**Running With Heuristic:**

Type the following command in the terminal:

```bash
python find_route.py <input_file/filepath> <origin> <destination> <heuristic_file/filepath>
```

*Note: Replace `<input_file/filepath>`, `<origin>`, `<destination>`, and `<heuristic_file/filepath>` with the appropriate values.*

## Example Runs

### Example 1 - Without Heuristic

```bash
python find_route.py input1.txt Bremen Kassel
```

**Output:**

```text
Uninformed_search
Nodes Popped: 8
Nodes Expanded: 6
Nodes Generated: 13
Distance: 297.0 km
Route:
Bremen to Hannover, 132.0 km
Hannover to Kassel, 165.0 km
```

### Example 2 - Without Heuristic & No Route Found

```bash
python find_route.py input1.txt London Kassel
```

**Output:**

```text
Uninformed_search
Nodes Popped: 4
Nodes Expanded: 4
Nodes Generated: 3
Distance: infinity
Route:
None
```

### Example 3 - With Heuristic

```bash
python find_route.py input1.txt Bremen Kassel h_kassel.txt
```

**Output:**

```text
Informed Search
Nodes Popped: 3
Nodes Expanded: 2
Nodes Generated: 6
Distance: 297.0 km
Route:
Bremen to Hannover, 132.0 km
Hannover to Kassel, 165.0 km
```

### Example 4 - With Heuristic & No Route Found

```bash
python find_route.py input1.txt London Kassel h_kassel.txt
```

**Output:**

```text
Informed Search
Nodes Popped: 4
Nodes Expanded: 4
Nodes Generated: 3
Distance: infinity
Route:
None
```
