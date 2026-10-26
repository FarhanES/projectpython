"""
MINI PROJECT ASSIGNMENT
TIC-TAC-TOE GAME USING PYTHON
Two-player, console-based application

README / HOW TO RUN
1. Save this file as tic_tac_toe.py.
2. Install Python 3.x if it is not already installed.
3. Open a terminal or command prompt in the folder containing this file.
4. Run: python tic_tac_toe.py
   On some systems, use: python3 tic_tac_toe.py
5. Follow the on-screen instructions to play.

PROJECT OBJECTIVE
Create a two-player Tic-Tac-Toe game in the console using Python fundamentals:
variables, data types, functions, loops, conditional statements, lists, input
validation, exception handling, and formatted output. No external libraries or
database are required.

GAME RULES
- The board has 3 rows and 3 columns.
- Player 1 uses X and Player 2 uses O.
- Players take turns choosing an empty cell numbered 1 through 9.
- Three matching symbols in a row, column, or diagonal wins.
- If all nine cells are filled without a winner, the game is a draw.
- After each round, players can choose to play again.

PROJECT REQUIREMENTS INCLUDED
- Console board with row/column separators and cell numbers.
- Two-player turn handling.
- Move input from 1 to 9.
- Validation for empty, non-numeric, out-of-range, and occupied-cell input.
- Win detection for all rows, columns, and diagonals.
- Draw detection and final-board display.
- Play-again option that resets the board.
- Score tally across rounds and player-chosen names (bonus features).
- Functions, loops, lists, exception handling, and comments.
- Uses only Python's standard language features; no external packages.

EVALUATION RUBRIC (50 MARKS, FROM ASSIGNMENT)
- Board Display & Game Logic: 15
- Turn Handling & Move Input: 10
- Win & Draw Detection: 10
- Input Validation & Error Handling: 8
- Code Quality & Documentation: 7
"""

def create_board():
    """Return a fresh 3 x 3 board containing empty cells."""
    return [[" " for _ in range(3)] for _ in range(3)]


def display_board(board):
    """Display the board and the cell numbers used to make a move."""
    print()
    print("       TIC-TAC-TOE")
    print("  Cell numbers: 1 to 9")
    print()
    cell = 1
    for row_index, row in enumerate(board):
        display_row = []
        for value in row:
            # Show the cell number when the cell is still empty.
            display_row.append(value if value != " " else str(cell))
            cell += 1
        print("       " + " | ".join(display_row))
        if row_index < 2:
            print("      ---+---+---")
    print()


def get_move(board, player_name, symbol):
    """Ask for a valid empty cell and return its row and column."""
    while True:
        choice = input(f"{player_name} ({symbol}), choose a cell (1-9): ").strip()

        # Reject empty input without changing the current player's turn.
        if not choice:
            print("Input cannot be empty. Please enter a number from 1 to 9.")
            continue

        # Catch non-numeric input instead of allowing the program to crash.
        try:
            cell_number = int(choice)
        except ValueError:
            print("Invalid input. Please enter a whole number from 1 to 9.")
            continue

        if cell_number < 1 or cell_number > 9:
            print("Out of range. Choose a cell from 1 to 9.")
            continue

        # Convert the cell number to zero-based row and column indexes.
        row = (cell_number - 1) // 3
        column = (cell_number - 1) % 3

        if board[row][column] != " ":
            print("That cell is already occupied. Choose an empty cell.")
            continue

        return row, column


def has_won(board, symbol):
    """Return True if the given symbol has a complete row, column, or diagonal."""
    # Check all three rows.
    for row in board:
        if all(cell == symbol for cell in row):
            return True

    # Check all three columns.
    for column in range(3):
        if all(board[row][column] == symbol for row in range(3)):
            return True

    # Check the two diagonals.
    if all(board[index][index] == symbol for index in range(3)):
        return True

    if all(board[index][2 - index] == symbol for index in range(3)):
        return True

    return False


def board_is_full(board):
    """Return True when there are no empty cells left."""
    return all(cell != " " for row in board for cell in row)


def play_round(players, scores):
    """Run one complete round and return the winning player's index, or None for a draw."""
    board = create_board()
    current_player = 0

    while True:
        display_board(board)
        player_name, symbol = players[current_player]
        row, column = get_move(board, player_name, symbol)
        board[row][column] = symbol

        # Check for a win immediately after the move.
        if has_won(board, symbol):
            display_board(board)
            print(f"Congratulations, {player_name}! You win this round.")
            scores[current_player] += 1
            return current_player

        # A draw is possible only after checking that the last move did not win.
        if board_is_full(board):
            display_board(board)
            print("The game is a draw. Nobody wins this round.")
            return None

        # Switch to the other player.
        current_player = 1 - current_player


def ask_to_play_again():
    """Return True for yes and False for no; validate the answer."""
    while True:
        answer = input("Would you like to play another round? (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please enter y/yes or n/no.")


def main():
    """Set up players and keep running rounds until the players choose to exit."""
    print("=" * 42)
    print("       TIC-TAC-TOE GAME")
    print("      Python Mini Project")
    print("=" * 42)

    # Bonus feature: allow players to enter their own names.
    player_one = input("Enter Player 1 name (X): ").strip() or "Player 1"
    player_two = input("Enter Player 2 name (O): ").strip() or "Player 2"

    players = [(player_one, "X"), (player_two, "O")]
    scores = [0, 0]
    round_number = 1

    while True:
        print(f"\n--- Round {round_number} ---")
        play_round(players, scores)

        # Bonus feature: maintain the score across multiple rounds.
        print("\nSCOREBOARD")
        print(f"{players[0][0]} (X): {scores[0]}")
        print(f"{players[1][0]} (O): {scores[1]}")

        if not ask_to_play_again():
            break

        round_number += 1

    print("\nFinal Score")
    print(f"{players[0][0]} (X): {scores[0]}")
    print(f"{players[1][0]} (O): {scores[1]}")
    print("Thank you for playing Tic-Tac-Toe. Goodbye!")


if __name__ == "__main__":
    main()
