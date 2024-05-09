"""Python script that calculates the posterior probabilities of different hypotheses from a given sequence of observations"""  # noqa: E501

import argparse
import logging
import sys

from logging import Logger, LogRecord
from pathlib import Path
from types import TracebackType
from typing import ClassVar, Literal


class ArgparseLogger(argparse.ArgumentParser):
    """Subclass of argparse.ArgumentParser that logs errors using a custom logger."""

    def __init__(self, logger, *args, **kwargs) -> None:  # noqa: ANN003, ANN002, ANN001
        """Initialize the ArgparseLogger class.

        Args:
            logger: The custom logger to be used.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.logger = logger

    def error(self, message: str) -> None:
        """Overrides the default error method to log parsing errors using the custom logger."""
        full_message = f"{self.prog}: error: {message}"
        self.logger.error(full_message)  # Log the actual argparse error message
        self.print_help(sys.stderr)
        self.exit(2, full_message + "\n")


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

    def format(self, record: LogRecord) -> str:
        """Format the specified record with color.

        Args:
            record (logging.LogRecord): The log record to be formatted.

        Returns:
            str: A formatted string with color based on the log level.
        """
        colored_record = logging.Formatter.format(self, record)
        levelno = record.levelno
        return f"{self.COLORS.get(levelno, '')}{colored_record}\033[0m"  # Reset to default


def _setup_custom_logger(name: str | None = None) -> Logger:
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


def calculate_likelihood(hypothesis: dict[str, float], observation: Literal["C", "L"]) -> float:
    """Calculate the likelihood P(observation | hypothesis) based on the candy type

    Arguments:
        hypothesis: A dictionary containing the probability distributions for both candy types
        observation: The observed candy type, 'C' for cherry and 'L' for lime

    Returns:
        float: The likelihood of the observation given the hypothesis
    """
    observation_key = "cherry" if observation == "C" else "lime"
    return hypothesis[observation_key]


def update_posterior(
    hypotheses: dict[str, dict[str, float]], observation: Literal["C", "L"]
) -> None:
    """Update the posterior probabilities of all hypotheses based on the given observation

    Arguments:
        hypotheses: A dictionary of all hypotheses with their current probabilities
        observation: The observed candy type, either 'C' or 'L'
    """
    total_prob = sum(
        hypothesis["prior"] * calculate_likelihood(hypothesis, observation)
        for hypothesis in hypotheses.values()
    )
    for hypothesis in hypotheses.values():
        likelihood = calculate_likelihood(hypothesis, observation)
        hypothesis["prior"] = (hypothesis["prior"] * likelihood) / total_prob


def next_candy_probability(
    hypotheses: dict[str, dict[str, float]], candy_type: Literal["cherry", "lime"]
) -> float | Literal[0]:
    """Calculate the probability of picking a specific type of candy next, given the updated hypotheses

    Arguments:
        hypotheses: A dictionary of all hypotheses with their updated probabilities
        candy_type: The type of candy ('cherry' or 'lime')

    Returns:
        float | Literal[0]: The probability of picking the specified type of candy next or 0 if the candy type is invalid
    """  # noqa: E501
    return sum(hypothesis["prior"] * hypothesis[candy_type] for hypothesis in hypotheses.values())


def calculate_posterior(hypotheses: dict[str, dict[str, float]], observations: str) -> None:
    """Calculate the posterior probabilities of all hypotheses based on the given observation sequence

    After each observation, the posterior probabilities are calculated and written to a file

    Arguments:
        hypotheses: A dictionary of all hypotheses with their initial probabilities and likelihoods
        observations: The sequence of observed candy types, either 'C' or 'L'
    """  # noqa: E501
    with Path.open("result.txt", "w") as file:
        file.write(f"Observation sequence Q: {observations}\n")
        file.write(f"Length of Q: {len(observations)}\n\n")

        for index, observation in enumerate(observations):
            update_posterior(hypotheses, observation)
            file.write(f"After Observation {index + 1} = {observation}:\n\n")

            for h_name, h_data in hypotheses.items():
                file.write(f"P({h_name} | Q) = {h_data['prior']:.5g}\n")

            file.write(
                f"\nProbability that the next candy we pick will be C, given Q: "
                f"{next_candy_probability(hypotheses, 'cherry'):.5g}\n"
            )
            file.write(
                f"Probability that the next candy we pick will be L, given Q: "
                f"{next_candy_probability(hypotheses, 'lime'):.5g}\n\n"
            )


def _parse_args(custom_logger: logging.Logger) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = ArgparseLogger(
        custom_logger,
        description=" Python script that calculates the posterior probabilities of different hypotheses from a given sequence of observations",  # noqa: E501
    )
    parser.add_argument(
        "observation",
        nargs="?",
        type=str,
        default="",
        help="The observation sequence",
    )
    return parser.parse_args()


def main() -> None:
    """Main function to read the observation sequence from the command line argument and calculate the posterior probabilities"""  # noqa: E501
    custom_logger = _setup_custom_logger()

    args = _parse_args(custom_logger)

    observations: str = args.observation

    hypotheses = {
        "h1": {"prior": 0.10, "cherry": 1.00, "lime": 0.00},
        "h2": {"prior": 0.20, "cherry": 0.75, "lime": 0.25},
        "h3": {"prior": 0.40, "cherry": 0.50, "lime": 0.50},
        "h4": {"prior": 0.20, "cherry": 0.25, "lime": 0.75},
        "h5": {"prior": 0.10, "cherry": 0.00, "lime": 1.00},
    }

    calculate_posterior(hypotheses, observations)


if __name__ == "__main__":
    main()
