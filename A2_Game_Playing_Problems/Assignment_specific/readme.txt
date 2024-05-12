Programming Language: Python 3.12.1

Code Structure:

    Classes:
        - class ArgparseLogger(argparse.ArgumentParser):
            """Subclass of argparse.ArgumentParser that logs errors using a custom logger."""

            - Methods:
                - def __init__(self, logger, *args, **kwargs) -> None:
                    """Initialize the ArgparseLogger class.

                    Args:
                        logger: The custom logger to be used.
                        *args: Additional positional arguments.
                        **kwargs: Additional keyword arguments.
                    """

                - def error(self, message: str) -> None:
                    """Overrides the default error method to log parsing errors using the custom logger."""

        - class ColorLogFormatter(logging.Formatter):
            """A custom log formatter that adds color to log levels.

            Attributes:
                fmt (str): The format string used to format the log message.
                COLORS (dict): A dictionary mapping log levels to their respective ANSI color codes.
            """

            - Methods:
                - def format(self, record: LogRecord) -> str:
                    """Format the specified record with color.

                    Args:
                        record (logging.LogRecord): The log record to be formatted.

                    Returns:
                        str: A formatted string with color based on the log level.
                    """

        - class GameState:
            """Class to represent the current state of the Red-Blue Nim game."""

            - Methods:
                - def __init__(self, red_marbles: int, blue_marbles: int, version: str) -> None:
                    """Initialize the GameState with a specified number of red and blue marbles, and game version.

                    Args:
                        red_marbles (int): The initial number of red marbles.
                        blue_marbles (int): The initial number of blue marbles.
                        version (str): The version of the game (e.g., 'standard', 'misere').
                    """

                - def is_game_over(self) -> bool:
                    """Determine if the game is over based on the marble counts.

                    Returns:
                        bool: True if either the red or blue marbles count is zero, False otherwise.
                    """

                - def execute_move(self, move: tuple[str, int]) -> None:
                    """Execute a game move by updating the state of the marbles.

                    Args:
                        move (tuple[str, int]): The move to be made, specified as a tuple with color ('red' or 'blue') and count.
                    """

    Functions:
        - def evaluate_state(game_state: GameState) -> int:
            """Evaluate and return a score for the current game state.

            Args:
                game_state (GameState): The current state of the game.

            Returns:
                int: The calculated score for the current game state.
            """

        - def valid_moves(game_state: GameState, version: str) -> list:
            """Generate a list of valid moves based on the current game state and version.

            Args:
                game_state (GameState): The current state of the game.
                version (str): The version of the game (e.g., 'standard', 'misere').

            Returns:
                list: A list of valid moves, each represented as a tuple (color, count).
            """

        - def minmax(game_state: GameState, depth: int, alpha: int, beta: int, maximizing_player: bool) -> tuple[int, tuple[str, int] | None]:
            """Minimax algorithm with alpha-beta pruning for decision making in the game.

            Args:
                game_state (GameState): The current state of the game.
                depth (int): The maximum depth of the search tree.
                alpha (int): The alpha value for alpha-beta pruning.
                beta (int): The beta value for alpha-beta pruning.
                maximizing_player (bool): True if the current move is by the maximizing player, False otherwise.

            Returns:
                tuple[int, tuple[str, int] | None]: A tuple of the best score and the corresponding best move.
            """

        - def human_turn() -> tuple[str, int]:
            """Handle the human player's turn, prompting for and validating their move.

            Returns:
                tuple[str, int]: The human player's move as a tuple (color, count).
            """

        - def computer_turn(game_state: GameState, move: tuple[str, int]) -> None:
            """Display the computer's move.

            Arguments:
                game_state (GameState): The current state of the game.
                move (tuple[str, int]): The move made by the computer (color, count).
            """

        - def red_blue_nim(red_marbles: int, blue_marbles: int, version: str, first_player: str, depth: int) -> None:
            """Main function to manage the flow of the Red-Blue Nim game.

            Args:
                red_marbles (int): The initial number of red marbles.
                blue_marbles (int): The initial number of blue marbles.
                version (str): The version of the game (e.g., 'standard', 'misere').
                first_player (str): The first player ('human' or 'computer').
                depth (int): The depth for the minimax search algorithm.
            """

        - def _setup_custom_logger(log_file: bool = False) -> Logger:
            """Sets up a global logger with custom formatting and a global exception handler."""

        - def _parse_args(logger: Logger) -> argparse.Namespace:
            """Parse command-line arguments for the Red-Blue Nim game.

            Arguments:
                logger (Logger): The logger object.

            Returns:
                argparse.Namespace: The parsed arguments.
            """

        - def main() -> None:
            """Main function to parse command-line arguments and start the Red-Blue Nim game."""

How to Run the Script:
    1. Open a terminal window.

    2. Navigate to the directory containing the 'red_blue_nim.py' script.

    3. The command-line arguments are as follows:
            - The initial number of red marbles
            - The initial number of blue marbles
            - The game version ('standard' or 'misere') (Default: 'standard')
            - The first player ('human' or 'computer') (Default: 'computer')
            - The depth for the minimax search algorithm (Default: '15')

        Run the script using the following command:
            python red_blue_nim.py 9 10 standard computer 15

        or using defaults:

            python red_blue_nim.py 9 10

        Note: You can show the help menu by running the script with '-h' or '--help' flag.

    4. Follow the prompts to play the game.
