"""This module custom utilities for logging and argument parsing."""

import argparse
import logging
import sys

from logging import Logger, LogRecord
from types import TracebackType
from typing import ClassVar


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
        logging.DEBUG: "\u001b[36;1m",  # Cyan for DEBUG
        logging.INFO: "\u001b[32;1m",  # Green for INFO
        logging.WARNING: "\u001b[33;1m",  # Yellow for WARNING
        logging.ERROR: "\u001b[31;1m",  # Red for ERROR
        logging.CRITICAL: "\u001b[1m\u001b[31m",  # Bold Red for CRITICAL
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
        return f"{self.COLORS.get(levelno, '')}{colored_record}\u001b[0m"  # Reset to default


def setup_custom_logger(log_file: bool = False) -> Logger:
    """Sets up a global logger with custom formatting and a global exception handler."""
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()
    formatter = ColorLogFormatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    if log_file:
        file_handler = logging.FileHandler("logfile.log")
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        logger.addHandler(file_handler)

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
