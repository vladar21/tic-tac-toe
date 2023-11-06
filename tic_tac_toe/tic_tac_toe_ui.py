"""
This module is responsible for the user interface of the tic-tac-toe game.
It contains functions to display the game board, start screen,
and leaderboard to the user.
"""


def display_start_game():
    """
    Display the starting information for the game, including rules and the
    initial game board.
    """

    print("Game rules:")
    print("Your turn will have symbol 'X', the AI turn - symbol 'O'.")
    print(
        "The winner must have three of their symbols in a line, vertically"
        " or horizontally."
    )
    print("\nGameplay field: ")
    start_board = ["0", "1", "2", "3", "4", "5", "6", "7", "8"]
    print(f"\n {start_board[0]} | {start_board[1]} | {start_board[2]} ")
    print(" --------- ")
    print(f" {start_board[3]} | {start_board[4]} | {start_board[5]} ")
    print(" --------- ")
    print(f" {start_board[6]} | {start_board[7]} | {start_board[8]} ")


def print_row(row_board, row_numbers):
    """
    Converts board row values to symbols and aligns them
    with their respective cell numbers.
    """

    # Define a dictionary to map numeric values to 'X', 'O', or a blank space
    value_to_symbol = {1: 'X', -1: 'O', 0: ' '}

    # Convert the row values from numeric to their symbol representations
    row_board_symbols = [value_to_symbol[item] for item in row_board]
    row_numbers_str = [str(item) for item in row_numbers]

    # Join the symbols and numbers into strings,
    # adding extra spaces for alignment
    # Adjust the number of spaces (' ' * n) as needed for the desired alignment
    return (' ' * 2 + ' | '.join(row_board_symbols) +
            ' ' * 11 + ' | '.join(row_numbers_str))


def display_board(board):
    """
    Displays the game board with current plays and
    a reference board with cell numbers.
    Used cells on the reference board are replaced with an asterisk ( * )
    """
    # Create a copy of the board with cell numbers
    numbers_board = [[str(i + j * 3) for i in range(3)] for j in range(3)]

    # Replace numbers with '*' in the numbers_board where
    # the corresponding cell in the board is not empty
    for y in range(3):
        for x in range(3):
            # Assuming 0 is the value for an empty space
            if board[y][x] != 0:
                # Assuming you want to display '*' for filled spaces
                numbers_board[y][x] = '*'

    # Print the board with headers for user guidance
    print("Current board:       Positions:")
    for i in range(3):
        # Print each row of the board
        print(print_row(board[i], numbers_board[i]))
        if i < 2:  # Print the row separator if it's not the last row
            print(" ---+---+---         ---+---+---")


def display_leadersboard(leadersboard_data_sheet, current_player_nickname):
    """
    Fetch and display the leadersboard with the rankings based on
    past game outcomes. The current player's row will be highlighted.
    """

    # Fetching the data from the sheet
    leadersboard_data = leadersboard_data_sheet.get_all_values()

    print("\nLeadersboard")

    # Headers for the table
    headers = [
        "PP",
        "Human Nickname",
        "Total Games",
        "Win Human",
        "Win AI",
        "Draw"
        ]

    # Define ANSI codes for highlighting
    HIGHLIGHT_START = "\033[93m"  # Yellow text
    HIGHLIGHT_END = "\033[0m"     # Reset to default text color

    # If there are no data rows or only header row,
    # print the headers and return
    if len(leadersboard_data) <= 1:
        print(" | ".join(headers))
        return

    # Sort the data by 'Win Human' column in descending order,
    # skipping the header
    # Make sure to convert 'Win Human' values to integers for sorting
    leadersboard_data[1:] = sorted(
        leadersboard_data[1:], key=lambda x: int(x[2]), reverse=True
    )

    # Determine the maximum width for each column
    column_lengths = [len(header) for header in headers]
    for row in leadersboard_data[1:]:  # Skip the header row in the data
        for i, (item, header) in enumerate(zip(row, headers)):
            column_lengths[i] = max(column_lengths[i], len(item))

    # Create a format string for each row with appropriate spacing
    row_format = " | ".join(
        [
            "{:<" + str(length) + "}" for length in column_lengths
        ]
    )

    # Print the formatted header row
    print(row_format.format(*headers))
    # Print header separator
    print("-" * (sum(column_lengths) + 3 * (len(headers) - 1)))

    # Print the sorted and formatted data rows,
    # skipping the first row which is headers
    for i, row_data in enumerate(leadersboard_data[1:], start=1):
        # If the row has less columns than headers, append empty strings
        row_data += [""] * (len(headers) - len(row_data))
        formatted_row = row_format.format(i, *row_data)
        # Highlight the current player's row
        if row_data[0] == current_player_nickname:
            formatted_row = HIGHLIGHT_START + formatted_row + HIGHLIGHT_END
        # Print each row with the correct number for 'PP'
        print(formatted_row)
