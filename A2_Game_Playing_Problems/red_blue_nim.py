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


class GameState:
    """Class to represent the current state of the Red-Blue Nim game."""

    def __init__(self, red_marbles: int, blue_marbles: int, version: str) -> None:
        """Initialize the GameState with a specified number of red and blue marbles, and game version.

        Args:
            red_marbles (int): The initial number of red marbles.
            blue_marbles (int): The initial number of blue marbles.
            version (str): The version of the game (e.g., 'standard', 'misere').
        """  # noqa: E501
        self.red_marbles = red_marbles
        self.blue_marbles = blue_marbles
        self.version = version

    def is_game_over(self) -> bool:
        """Determine if the game is over based on the marble counts.

        Returns:
            bool: True if either the red or blue marbles count is zero, False otherwise.
        """
        return self.red_marbles == 0 or self.blue_marbles == 0

    def execute_move(self, move: tuple[str, int]) -> None:
        """Execute a game move by updating the state of the marbles.

        Args:
            move (tuple[str, int]): The move to be made, specified as a tuple with color ('red' or 'blue') and count.
        """  # noqa: E501
        if move[0] == "red":
            self.red_marbles = max(0, self.red_marbles - move[1])
        elif move[0] == "blue":
            self.blue_marbles = max(0, self.blue_marbles - move[1])


def evaluate_state(game_state: GameState) -> int:
    """Evaluate and return a score for the current game state.

    Args:
        game_state (GameState): The current state of the game.

    Returns:
        int: The calculated score for the current game state.
    """
    if game_state.version == "standard":
        total_marbles = game_state.red_marbles + game_state.blue_marbles

        # Prioritize reducing piles but not emptying them
        reduction_score = -(total_marbles)

        # Heavy penalty for leaving just 1 or 2 marbles in a pile
        near_loss_penalty = 0
        if game_state.red_marbles in {1, 2} or game_state.blue_marbles in {1, 2}:
            near_loss_penalty = -500

        # Maintain a certain balance between piles to avoid easy wins for the opponent
        balance_score = 0
        if abs(game_state.red_marbles - game_state.blue_marbles) >= 3:
            balance_score = -100

        return reduction_score + near_loss_penalty + balance_score

    # misere version
    return -abs(game_state.red_marbles - game_state.blue_marbles)


def valid_moves(game_state: GameState, version: str) -> list:
    """Generate a list of valid moves based on the current game state and version.

    Args:
        game_state (GameState): The current state of the game.
        version (str): The version of the game (e.g., 'standard', 'misere').

    Returns:
        list: A list of valid moves, each represented as a tuple (color, count).
    """
    moves = []
    if game_state.red_marbles >= 2:
        moves.append(("red", 2))
    if game_state.blue_marbles >= 2:
        moves.append(("blue", 2))
    if game_state.red_marbles >= 1:
        moves.append(("red", 1))
    if game_state.blue_marbles >= 1:
        moves.append(("blue", 1))

    # If misere version, invert the order of moves
    if version == "misere":
        moves.reverse()

    return moves


def minmax(
    game_state: GameState, depth: int, alpha: int, beta: int, maximizing_player: bool
) -> tuple[int, tuple[str, int] | None]:
    """Minimax algorithm with alpha-beta pruning for decision making in the game.

    Args:
        game_state (GameState): The current state of the game.
        depth (int): The maximum depth of the search tree.
        alpha (int): The alpha value for alpha-beta pruning.
        beta (int): The beta value for alpha-beta pruning.
        maximizing_player (bool): True if the current move is by the maximizing player, False otherwise.

    Returns:
        tuple[int, tuple[str, int] | None]: A tuple of the best score and the corresponding best move.
    """  # noqa: E501
    if depth == 0 or game_state.is_game_over():
        return evaluate_state(game_state), None

    possible_moves = valid_moves(game_state, game_state.version)

    if maximizing_player:
        max_eval = float("-inf")
        best_move = None
        for move in possible_moves:
            new_state = GameState(
                game_state.red_marbles, game_state.blue_marbles, game_state.version
            )
            new_state.execute_move(move)
            evaluation, _ = minmax(new_state, depth - 1, alpha, beta, False)
            if evaluation > max_eval:
                max_eval = evaluation
                best_move = move
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        return max_eval, best_move

    min_eval = float("inf")
    best_move = None
    for move in possible_moves:
        new_state = GameState(game_state.red_marbles, game_state.blue_marbles, game_state.version)
        new_state.execute_move(move)
        evaluation, _ = minmax(new_state, depth - 1, alpha, beta, True)
        if evaluation < min_eval:
            min_eval = evaluation
            best_move = move
        beta = min(beta, evaluation)
        if beta <= alpha:
            break

    return min_eval, best_move


def human_turn(game_state: GameState) -> tuple[str, int]:
    """Handle the human player's turn, prompting for and validating their move.

    Returns:
        tuple[str, int]: The human player's move as a tuple (color, count).
    """
    print("\u001b[4m---- TOTAL MARBLES ----\u001b[0m \n")
    print(f"\u001b[31;1mRed Marbles: {game_state.red_marbles}\u001b[0m")
    print(f"\u001b[34;1mBlue Marbles: {game_state.blue_marbles}\u001b[0m \n")
    color_options: dict[int, str] = {1: "red 2", 2: "blue 2", 3: "red 1", 4: "blue 1"}
    while True:
        print(
            "Enter your move: \n  1: \u001b[31;1mred \u001b[33;1m2 \u001b[0m \n  2: \u001b[34;1mblue \u001b[33;1m2 \u001b[0m \n  3: \u001b[31;1mred \u001b[33;1m1 \u001b[0m \n  4: \u001b[34;1mblue \u001b[33;1m1 \u001b[0m \n"  # noqa: E501
        )
        user_input = input("Selection: ")
        if user_input.isdigit() and int(user_input) in color_options:
            user_input = color_options.get(int(user_input)).strip()
            color, count_str = user_input.split()
            count = int(count_str)
            return color, count
        print("\u001b[1m\u001b[4m\u001b[31;1mInvalid move. Try again. \u001b[0m \n")


def computer_turn(game_state: GameState, move: tuple[str, int]) -> None:
    """Display the computer's move.

    Arguments:
        game_state (GameState): The current state of the game.
        move (tuple[str, int]): The move made by the computer (color, count).
    """
    print("\u001b[30;1m==== COMPUTERS LOGIC ====\u001b[0m \n")
    print("\u001b[30;1m==== TOTAL MARBLES ====\u001b[0m \n")
    print(f"\u001b[30;1mRed Marbles: {game_state.red_marbles}\u001b[0m")
    print(f"\u001b[30;1mBlue Marbles: {game_state.blue_marbles}\u001b[0m \n")
    print("\u001b[30;1m==== COMPUTERS MOVE ====\u001b[0m \n")
    print(f"\u001b[30;1mColor: {move[0]}\u001b[0m")
    print(f"\u001b[30;1mNumber of Marbles: {move[1]}\u001b[0m \n")


def red_blue_nim(
    red_marbles: int, blue_marbles: int, version: str, first_player: str, depth: int
) -> None:
    """Main function to manage the flow of the Red-Blue Nim game.

    Args:
        red_marbles (int): The initial number of red marbles.
        blue_marbles (int): The initial number of blue marbles.
        version (str): The version of the game (e.g., 'standard', 'misere').
        first_player (str): The first player ('human' or 'computer').
        depth (int): The depth for the minimax search algorithm.
    """
    game_state = GameState(red_marbles, blue_marbles, version)
    current_player = first_player

    while not game_state.is_game_over():
        if current_player == "computer":
            _, move = minmax(game_state, depth, float("-inf"), float("inf"), True)
            computer_turn(game_state, move)
            game_state.execute_move(move)
            current_player = "human"
        else:
            move = human_turn(game_state)
            print("\n\u001b[4m---- YOUR MOVE ----\u001b[0m \n")
            if move[0] == "red":
                print(f"Color: \u001b[31;1m{move[0]}\u001b[0m")
            else:
                print(f"Color: \u001b[34;1m{move[0]}\u001b[0m")
            print(f"Number of Marbles: \u001b[33;1m {move[1]} \u001b[0m \n")
            game_state.execute_move(move)
            current_player = "computer"

    # Calculating the final score
    if game_state.version == "standard":
        winner = "Human" if current_player == "computer" else "Computer"
    else:  # misère
        winner = "Computer" if current_player == "computer" else "Human"

    score = 2 * game_state.red_marbles + 3 * game_state.blue_marbles
    print("\u001b[4m\u001b[36;1m~~~ Game over! ~~~\u001b[0m \n")
    print(f"\u001b[31;1mRed Marbles Left: {game_state.red_marbles}\u001b[0m")
    print(f"\u001b[34;1mBlue Marbles Left: {game_state.blue_marbles}\u001b[0m \n")
    print(f"\u001b[35;1m{winner}\u001b[36;1m wins with a score of \u001b[35;1m{score}\u001b[0m \n")


def _setup_custom_logger(log_file: bool = False) -> Logger:
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


def _parse_args(logger: Logger) -> argparse.Namespace:
    """Parse command-line arguments for the Red-Blue Nim game.

    Arguments:
        logger (Logger): The logger object.

    Returns:
        argparse.Namespace: The parsed arguments.
    """
    parser = ArgparseLogger(logger, description="Play Red-Blue Nim.")
    parser.add_argument("num_red", type=int, help="Number of red marbles")
    parser.add_argument("num_blue", type=int, help="Number of blue marbles")
    parser.add_argument(
        "version",
        nargs="?",
        default="standard",
        choices=["standard", "misere"],
        help="Game version (default: standard)",
    )
    parser.add_argument(
        "first_player",
        nargs="?",
        default="computer",
        choices=["computer", "human"],
        help="First player (default: computer)",
    )
    parser.add_argument(
        "depth",
        nargs="?",
        type=int,
        default=15,
        help="Depth for search, must be greater than 0 (default: 15)",
    )

    return parser.parse_args()


def main() -> None:
    """Main function to parse command-line arguments and start the Red-Blue Nim game."""
    logger = _setup_custom_logger()

    args = _parse_args(logger)

    if args.depth < 1:
        logger.error("Invalid depth argument. Depth must be greater than 0. Please try again. \n")
        sys.exit(1)

    red_blue_nim(args.num_red, args.num_blue, args.version, args.first_player, args.depth)


if __name__ == "__main__":
    main()
