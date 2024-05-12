# Task 2 - Bayesian Networks

## Programming Language

- Python 3.12.2

## Code Structure

### Classes

```python
BayesianNetwork()
```

### Class methods

```python
__init__(self) -> None
```

- Initializes the Bayesian Network with the given probabilities from the problem statement

```python
def compute_probability(self, b: bool, e: bool, a: bool, j: bool, m: bool) -> float
```

- Computes the joint probability of the given events

### Functions

```python
calculate_specified_probability(network: BayesianNetwork, c1: dict[str, bool], c2: dict[str, bool]) -> float
```

- Calculates the specified probability of the given events

```python
parse_arguments(args: list[str]) -> tuple[dict[str, bool], dict[str, bool]]
```

- Parses command line arguments to extract events and their states

```python
main() -> None
```

- Main function to compute the specified probability of the given events

## Running the Code

- Make sure you have Python 3.12.2 installed on your system (was not tested on any other versions)
- In the directory where the script is located, run the script using the following command:

```bash
python bayesian_network.py <event1><state1> <event2><state2> <event3><state3> <event4><state4> <event5><state5>
```

where:

- event1, event2, event3, event4, event5 are the events
- state1, state2, state3, state4, state5 are the states of the corresponding events

### Example Without Optional Argument

```bash
python bnet.py Bf At Mt
```

### Optional Argument

```bash
python bayesian_network.py <event1><state1> given <event2><state2> <event3><state3>
```

### Example With Optional Argument

```bash
python bnet.py Jt given Et Bf
```

```bash
python bnet.py Jf Mt given Et
```
