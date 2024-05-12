"""Module to compute the specified probability of the given events in a Bayesian Network"""

import logging
import sys

from itertools import product
from types import TracebackType
from typing import ClassVar


class ColorLogFormatter(logging.Formatter):
    """A custom log formatter that adds color to log levels.

    Attributes:
        fmt (str): The format string used to format the log message.
        COLORS (dict): A dictionary mapping log levels to their respective ANSI color codes.
    """

    COLORS: ClassVar[dict] = {
        logging.DEBUG: "\033[0;36m",  # Cyan for DEBUG
        logging.INFO: "\033[0;32m",  # Green for INFO
        logging.WARNING: "\033[0;33m",  # Yellow for WARNING
        logging.ERROR: "\033[0;31m",  # Red for ERROR
        logging.CRITICAL: "\033[1;31m",  # Bold Red for CRITICAL
    }

    def format(self, record: logging.LogRecord) -> str:
        """Format the specified record with color.

        Args:
            record (logging.LogRecord): The log record to be formatted.

        Returns:
            str: A formatted string with color based on the log level.
        """
        colored_record = logging.Formatter.format(self, record)
        levelno = record.levelno
        return f"{self.COLORS.get(levelno, '')}{colored_record}\033[0m"  # Reset to default


class BayesianNetwork:
    """Class to represent a Bayesian Network and compute the joint probability of events"""

    def __init__(self) -> None:
        """Initializes the Bayesian Network with the given probabilities from the problem statement"""  # noqa: E501
        self.p_b = 0.001  # Probability of Burglary being true
        self.p_e = 0.002  # Probability of Earthquake being true

        # Conditional probabilities for Alarm given Burglary and Earthquake
        self.p_a_b_e = {
            (True, True): 0.95,
            (True, False): 0.94,
            (False, True): 0.29,
            (False, False): 0.001,
        }

        # Conditional probabilities for JohnCalls and MaryCalls given Alarm
        self.p_j_a = {True: 0.90, False: 0.05}
        self.p_m_a = {True: 0.70, False: 0.01}

    def compute_probability(  # noqa: PLR0913
        self, b: bool, e: bool, a: bool, j: bool, m: bool
    ) -> float:
        """Computes the joint probability of the given events

        Arguments:
            b: Burglary event state
            e: Earthquake event state
            a: Alarm event state
            j: John Calls event state
            m: Mary Calls event state

        Returns:
            float: The joint probability of the events
        """
        p_b = self.p_b if b else 1 - self.p_b
        p_e = self.p_e if e else 1 - self.p_e
        p_a_given_b_e = self.p_a_b_e[(b, e)] if a else 1 - self.p_a_b_e[(b, e)]
        p_j_given_a = self.p_j_a[a] if j else 1 - self.p_j_a[a]
        p_m_given_a = self.p_m_a[a] if m else 1 - self.p_m_a[a]
        return p_b * p_e * p_a_given_b_e * p_j_given_a * p_m_given_a


def _setup_custom_logger(name: str | None = None) -> logging.Logger:
    """Sets up a global logger with custom formatting and a global exception handler."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()
    formatter = ColorLogFormatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Global exception handler
    def handle_exception(
        exc_type: type[BaseException], exc_value: BaseException, exc_traceback: TracebackType
    ) -> None:
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logger.critical(f"{exc_type}", exc_info=(exc_type, exc_value, exc_traceback))

    sys.excepthook = handle_exception
    return logger


def calculate_specified_probability(
    network: BayesianNetwork, c1: dict[str, bool], c2: dict[str, bool]
) -> float:
    """Calculates the specified probability of the given events

    Arguments:
        network: Bayesian Network object
        c1: Dictionary representing the first set of events
        c2: Dictionary representing the second set of events

    Returns:
        float: The calculated probability
    """
    if not c2:
        unspecified_vars = {k for k in "BEAJM" if k not in c1}
        all_combinations = product([True, False], repeat=len(unspecified_vars))
        total_prob = 0.0
        for combination in all_combinations:
            state = dict(zip(unspecified_vars, combination, strict=False))
            state.update(c1)
            total_prob += network.compute_probability(
                state["B"], state["E"], state["A"], state["J"], state["M"]
            )
        return total_prob

    joint_vars = {**c1, **c2}
    unspecified_vars = {k for k in "BEAJM" if k not in joint_vars}
    all_joint_combinations = product([True, False], repeat=len(unspecified_vars))
    joint_prob = 0.0

    for combination in all_joint_combinations:
        state = dict(zip(unspecified_vars, combination, strict=False))
        state.update(joint_vars)
        joint_prob += network.compute_probability(
            state["B"], state["E"], state["A"], state["J"], state["M"]
        )

    c2_only_vars = {k for k in "BEAJM" if k not in c2}
    all_c2_combinations = product([True, False], repeat=len(c2_only_vars))
    c2_prob = 0.0

    for combination in all_c2_combinations:
        state = dict(zip(c2_only_vars, combination, strict=False))
        state.update(c2)
        c2_prob += network.compute_probability(
            state["B"], state["E"], state["A"], state["J"], state["M"]
        )

    return joint_prob / c2_prob if c2_prob != 0 else 0


def _parse_arguments(args: list[str]) -> tuple[dict[str, bool], dict[str, bool]]:
    """Parses command line arguments to extract events and their states

    Arguments:
        args: List of command line arguments

    Returns:
        tuple[dict[str, bool], dict[str, bool]]: Tuple containing two dictionaries representing the events and their states
    """  # noqa: E501
    if "given" in args:
        index = args.index("given")
        events_c1 = args[:index]
        events_c2 = args[index + 1 :]  # noqa: E203, RUF100
    else:
        events_c1 = args
        events_c2 = []

    c1 = {event[0]: (event[1] == "t") for event in events_c1}
    c2 = {event[0]: (event[1] == "t") for event in events_c2}
    return c1, c2


def main() -> None:
    """Main function to compute the specified probability of the given events"""
    _setup_custom_logger()
    if len(sys.argv) < 2 or len(sys.argv) > 7:
        logging.critical(
            "Invalid number of arguments\n"
            "Usage: python bnet.py <event><state> [optional: 'given'] <event><state>\n"
            "Events: 'B' - Burglary, 'E' - Earthquake, 'A' - Alarm, 'J' - JohnCalls, 'M' - MaryCalls\n"  # noqa: E501
            "States: 't' - True, 'f' - False\n"
            "Example: python bnet.py Bt At Jt given Mt"
        )
        return
    args = sys.argv[1:]
    c1, c2 = _parse_arguments(args)
    network = BayesianNetwork()
    probability = calculate_specified_probability(network, c1, c2)
    print(f"The computed probability is: {probability}")


if __name__ == "__main__":
    main()
