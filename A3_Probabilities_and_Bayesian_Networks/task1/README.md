# Task 1 - Posterior Probabilities

## Programming Language

- Python 3.12.2

## Code Structure

- The code is structured into functions to calculate the likelihood, update the posterior probabilities, and calculate the probability of the next candy being of a certain type.
- The main function reads the observation sequence from the command line argument, initializes the hypotheses, and calculates the posterior probabilities based on the observations.

### Functions

```python
calculate_likelihood(hypothesis: dict[str, float], observation: Literal["C", "L"]) -> float
```

- Calculates the likelihood P(observation | hypothesis) based on the candy type

```python
update_posterior(hypotheses: dict[str, dict[str, float]], observation: Literal["C", "L"]) -> None
```

- Updates the posterior probabilities of all hypotheses based on the given observation

```python
next_candy_probability(hypotheses: dict[str, dict[str, float]], candy_type: Literal["cherry", "lime"]) -> float | Literal[0]
```

- Calculates the probability of picking a specific type of candy next, given the updated hypotheses

```python
calculate_posterior(hypotheses: dict[str, dict[str, float]], observations: str) -> None
```

- Calculates the posterior probabilities of all hypotheses based on the given observation sequence
- After each observation, the posterior probabilities are calculated and written to a file

```python
main()
```

- Reads the observation sequence from the command line argument
- Initializes the hypotheses and calculates the posterior probabilities based on the observations

### Utility Function

```python
_setup_custom_logger(name: str | None = None) -> Logger
```

- Sets up a global logger with custom formatting and a global exception handler

### Utility Classes

```python
ColorLogFormatter(logging.Formatter)
```

- A custom log formatter that adds color to log levels for better readability

```python
ArgparseLogger(argparse.ArgumentParser)
```

- Subclass of argparse.ArgumentParser that logs errors using a custom logger

## Running the Code

- Make sure you have Python 3.12.2 installed on your system (was not tested on any other versions)
- In the directory where the script is located, run the script using the following command:

```bash
python compute_a_posteriori.py <observation_sequence>
```
