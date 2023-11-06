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


def display_board(board):
    """
    Display the current state of the game board with symbols 'X', 'O',
    or empty spaces.
    """

    # Get the total number of rows
    num_rows = len(board)

    # Iterate over each row in the board
    for i, row in enumerate(board):
        # Print the row with 'X', 'O', or ' ' depending on the cell value
        print(
            " | ".join(
                [
                    "X" if cell == 1 else
                    "O" if cell == -1 else
                    " "
                    for cell in row
                ]
            )
        )

        # Print a horizontal line to separate the rows, except for the last row
        if i < num_rows - 1:
            print("-" * 9)
    print()  # Print a newline at the end for better formatting


def display_leadersboard(leadersboard_data_sheet):
    """
    Fetch and display the leadersboard with the rankings based on
    past game outcomes.
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
        # Print each row with the correct number for 'PP'
        print(row_format.format(i, *row_data))
