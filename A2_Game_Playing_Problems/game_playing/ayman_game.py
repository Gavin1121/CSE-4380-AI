from sys import argv


# Constants for move ordering
standardMoves = ["Red 2", "Blue 2", "Red 1", "Blue 1"]
misereMoves = standardMoves[::-1]


class nimGame:
    # Initializes the current game with the given arguments
    def __init__(self, numRed, numBlue, version="standard", firstPlayer="computer", depth=None) -> None:
        self.red = numRed
        self.blue = numBlue
        self.version = version
        self.player = firstPlayer
        self.depth = depth

    # Returns a move list that is available given the current state
    def actions(self, state):
        red, blue = state
        moves = []
        if red >= 2:
            moves.append("Red 2")
        if blue >= 2:
            moves.append("Blue 2")
        if red >= 1:
            moves.append("Red 1")
        if blue >= 1:
            moves.append("Blue 1")
        return moves

    # Returns the state after what happens from the move made
    def result(self, state, move):
        red, blue = state
        if move == "Red 2":
            return red - 2, blue
        if move == "Blue 2":
            return red, blue - 2
        if move == "Red 1":
            return red - 1, blue
        if move == "Blue 1":
            return red, blue - 1
        return None

    # Returns what the current state is after it reaches the terminal state
    def utility(self, state, player):
        red, blue = state
        if self.version == "standard":
            if red == 0 or blue == 0:
                if player == "computer":
                    return -2 * red - 3 * blue
                return 2 * red + 3 * blue
        elif self.version == "misere" and (red == 0 or blue == 0):
            if player == "computer":
                return 2 * red + 3 * blue
            return -2 * red - 3 * blue
        return 0

    # Tests if the state is in a terminal state, returns True if yes, returns False if no
    def terminalTest(self, state):
        red, blue = state
        return red == 0 or blue == 0

    # Determines what player is currently active in the state
    def to_move(self, state) -> str:
        return "computer" if self.player == "computer" else "human"

    # Prints the current score of the game
    def displayScore(self, state) -> None:
        print("\n>>> RED PILE: %d   |   BLUE PILE: %d <<<" % (state[0], state[1]))

    # Start the game
    def playGame(self) -> None:
        currPlayer = self.player
        state = (self.red, self.blue)

        while not self.terminalTest(state):
            self.displayScore(state)

            if currPlayer == "computer":
                print(">>> COMPUTER'S TURN")
                move = self.computerMove(state)
                print(">>> COMPUTER'S MOVE: ", move)
            else:
                print(">>> HUMAN TURN ")
                print(">>> SELECT A MOVE:", self.actions(state))
                move = input("Your move: ")
                while move not in self.actions(state):
                    print("ERROR! Please choose a valid move!")
                    move = input("Your move: ")

            state = self.result(state, move)
            currPlayer = "human" if currPlayer == "computer" else "computer"

        print("\n>>> GAME OVER! <<<")
        score = state[0] * 2 + state[1] * 3
        if self.version == "standard":
            winner = "Human" if currPlayer == "computer" else "Computer"
        else:  # misère
            winner = "Computer" if currPlayer == "computer" else "Human"
        print(f">>> {winner} has won with {score}! <<<")

    # Returns what the computer's move is using minmax with alpha-beta pruning
    def computerMove(self, state):
        bestMove = None
        bestEval = float("-inf")
        alpha = float("-inf")
        beta = float("inf")
        moves = self.actions(state)

        moveOrder = standardMoves
        moveOrder = standardMoves if self.version == "standard" else misereMoves

        for move in moveOrder:
            if move in moves:
                newState = self.result(state, move)
                eval = self.minmax(newState, False, alpha, beta, self.depth)
                if eval > bestEval:
                    bestEval = eval
                    bestMove = move
        return bestMove

    # Minmax function with alpha-beta pruning
    def minmax(self, state, maxPlayer, alpha, beta, depth):
        if self.terminalTest(state):
            if maxPlayer:
                return self.utility(state, "computer")
            return self.utility(state, "human")

        if depth is None or depth == 0:
            if maxPlayer:
                maxEval = float("-inf")
                for move in self.actions(state):
                    newState = self.result(state, move)
                    eval = self.minmax(newState, False, alpha, beta, None)
                    maxEval = max(maxEval, eval)
                return maxEval
            minEval = float("inf")
            for move in self.actions(state):
                newState = self.result(state, move)
                eval = self.minmax(newState, True, alpha, beta, None)
                minEval = min(minEval, eval)
            return minEval

        if maxPlayer:
            maxEval = float("-inf")
            for move in self.actions(state):
                newState = self.result(state, move)
                eval = self.minmax(newState, False, alpha, beta, depth - 1)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval
        minEval = float("inf")
        for move in self.actions(state):
            newState = self.result(state, move)
            eval = self.minmax(newState, True, alpha, beta, depth - 1)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval


if __name__ == "__main__":
    numRed = int(argv[1])
    numBlue = int(argv[2])
    version = "standard" if len(argv) < 4 else argv[3]
    player = "computer" if len(argv) < 5 else argv[4]
    depth = None if len(argv) < 6 else int(argv[5])

    print(">>> WELCOME TO THE GAME! LET'S PLAY! <<<")
    game = nimGame(numRed, numBlue, version, player, depth)
    game.playGame()
