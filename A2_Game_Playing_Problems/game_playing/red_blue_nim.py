import logging

from game_playing import ArgparseLogger, setup_custom_logger


class GameState:
    def __init__(self, red_marbles: int, blue_marbles: int, version: str) -> None:
        self.red_marbles = red_marbles
        self.blue_marbles = blue_marbles
        self.version = version

    def is_game_over(self) -> bool:
        return self.red_marbles == 0 or self.blue_marbles == 0

    def execute_move(self, move: tuple[str, int]) -> None:
        if move[0] == "red":
            self.red_marbles = max(0, self.red_marbles - move[1])
        elif move[0] == "blue":
            self.blue_marbles = max(0, self.blue_marbles - move[1])


def evaluate_state(game_state: GameState) -> int:
    if game_state.version == "standard":
        return -(2 * game_state.red_marbles + 3 * game_state.blue_marbles)
    # misère
    return -abs(game_state.red_marbles - game_state.blue_marbles)


# Function to generate valid moves based on the current game state and version
def valid_moves(game_state: GameState, version: str) -> list:
    moves = []
    if game_state.red_marbles >= 2:
        moves.append(("red", 2))
    if game_state.blue_marbles >= 2:
        moves.append(("blue", 2))
    if game_state.red_marbles >= 1:
        moves.append(("red", 1))
    if game_state.blue_marbles >= 1:
        moves.append(("blue", 1))

    # In misère version, invert the order of moves
    if version == "misere":
        moves.reverse()

    return moves


def minmax(
    game_state: GameState, depth: int, alpha: int, beta: int, maximizing_player: bool
) -> tuple[int, tuple[str, int] | None]:
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
            eval, _ = minmax(new_state, depth - 1, alpha, beta, False)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float("inf")
        best_move = None
        for move in possible_moves:
            new_state = GameState(
                game_state.red_marbles, game_state.blue_marbles, game_state.version
            )
            new_state.execute_move(move)
            eval, _ = minmax(new_state, depth - 1, alpha, beta, True)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move


def human_turn(game_state: GameState) -> tuple[str, int]:
    color_options: dict[int, str] = {1: "red 2", 2: "blue 2", 3: "red 1", 4: "blue 1"}
    while True:
        print("Enter your move: \n  1: red 2 \n  2: blue 2 \n  3: red 1 \n  4: blue 1 \n")
        user_input = input("Selection: ")
        user_input = color_options.get(int(user_input)).strip()
        color, count_str = user_input.split()
        count = int(count_str)
        if color in {"red", "blue"} and count in {1, 2}:
            if (color == "red" and game_state.red_marbles >= count) or (
                color == "blue" and game_state.blue_marbles >= count
            ):
                return color, count
        print("Invalid move. Try again.")


def red_blue_nim(
    red_marbles: int, blue_marbles: int, version: str, first_player: str, depth: int
) -> None:
    game_state = GameState(red_marbles, blue_marbles, version)
    current_player = first_player

    while not game_state.is_game_over():
        print("\u001b[4m---- TOTAL MARBLES ----\u001b[0m \n")
        print(f"\u001b[31;1mRed Marbles: {game_state.red_marbles}\u001b[0m")
        print(f"\u001b[34;1mBlue Marbles: {game_state.blue_marbles}\u001b[0m \n")

        if current_player == "computer":
            _, move = minmax(game_state, depth, float("-inf"), float("inf"), True)
            print("\u001b[4m---- COMPUTERS MOVE ----\u001b[0m \n")
            print(f"Color: {move[0]}")
            print(f"Number of Marbles: {move[1]} \n")
            game_state.execute_move(move)
            current_player = "human"
        else:
            move = human_turn(game_state)
            print("\u001b[4m---- HUMANS MOVE ----\u001b[0m \n")
            print(f"Color: {move[0]}")
            print(f"Number of Marbles: {move[1]} \n")
            game_state.execute_move(move)
            current_player = "computer"

    # Calculating the final score
    if game_state.version == "standard":
        winner = "Human" if current_player == "computer" else "Computer"
    else:  # misère
        winner = "Computer" if current_player == "computer" else "Human"

    score = 2 * game_state.red_marbles + 3 * game_state.blue_marbles
    print(f"Game over! {winner} wins with a score of {score}")


if __name__ == "__main__":
    logger = setup_custom_logger()
    parser = ArgparseLogger(logger, description="Play Red-Blue Nim.")
    parser.add_argument("num_red", type=int, help="Number of red marbles")
    parser.add_argument("num_blue", type=int, help="Number of blue marbles")
    parser.add_argument(
        "version",
        nargs="?",
        default="standard",
        choices=["standard", "misere"],
        help="Game version",
    )
    parser.add_argument(
        "first_player",
        nargs="?",
        default="computer",
        choices=["computer", "human"],
        help="First player",
    )
    parser.add_argument("depth", nargs="?", type=int, default=10, help="Depth for search")
    args = parser.parse_args()

    red_blue_nim(args.num_red, args.num_blue, args.version, args.first_player, args.depth)
