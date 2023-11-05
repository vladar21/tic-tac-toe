def display_start_game():
    print('Game rules:')
    print("Your turn will have symbol 'X', the AI turn - symbol 'O'.")
    print("The winner must have three of their symbols in a line, vertically or horizontally.")
    print("\nGameplay field: ")
    start_board = ['0', '1', '2', '3', '4', '5', '6', '7', '8']
    print(f"\n {start_board[0]} | {start_board[1]} | {start_board[2]} ")
    print(" --------- ")
    print(f" {start_board[3]} | {start_board[4]} | {start_board[5]} ")
    print(" --------- ")
    print(f" {start_board[6]} | {start_board[7]} | {start_board[8]} ")

def display_board(board):

    # Get the total number of rows
    num_rows = len(board)

    # Iterate over each row in the board
    for i, row in enumerate(board):
        # Print the row with 'X', 'O', or ' ' depending on the cell value
        print(" | ".join(["X" if cell == 1 else "O" if cell == -1 else " " for cell in row]))
        
        # Print a horizontal line to separate the rows, except for the last row
        if i < num_rows - 1:
            print("-" * 9)
    print()  # Print a newline at the end for better formatting

def display_leadersboard(leadersboard_data_sheet):

    # Fetching the data from the sheet
    leadersboard_data = leadersboard_data_sheet.get_all_values()
    
    print("\nLeadersboard")

    # Headers for the table
    headers = ["PP", "Human Nickname", "Total Games", "Win Human", "Win AI", "Draw"]  # Added "Draw" to headers

    # If there are no data rows or only header row, print the headers and return
    if len(leadersboard_data) <= 1:
        print(" | ".join(headers))
        return

    # Determine the maximum width for each column
    column_lengths = [len(header) for header in headers]
    for row in leadersboard_data[1:]:  # Skip the header row in the data
        for i in range(len(row)):
            column_lengths[i] = max(column_lengths[i], len(row[i]))

    # Create a format string for each row with appropriate spacing
    row_format = " | ".join(["{:<" + str(length) + "}" for length in column_lengths])

    # Print the formatted header row
    print(row_format.format(*headers))
    print("-" * (sum(column_lengths) + 3 * (len(headers) - 1)))  # Print header separator

    # Print the formatted data rows, skipping the first row which is headers
    for i, row_data in enumerate(leadersboard_data[1:], start=1):  # Start with 1 to skip header row
        # If the row has less columns than headers, append empty strings
        row_data += [""] * (len(headers) - len(row_data))
        print(row_format.format(i, *row_data))  # Use row_data instead of row for clarity

def update_leadersboard(leadersboard_data_sheet, nickname, result):

    # Fetching the current data from the sheet
    leadersboard_data = leadersboard_data_sheet.get_all_values()
    headers = leadersboard_data[0]  # Assuming the first row contains headers

    # Find the indexes for the relevant columns
    nickname_index = headers.index("human_nickname") + 1  # +1 for Google Sheets indexing
    total_index = headers.index("total_games") + 1
    win_index = headers.index("win_human") + 1
    lose_index = headers.index("win_ai") + 1
    draws_index = headers.index("draws") + 1

    # Find the player in the leaderboard
    player_row = None
    for i, row in enumerate(leadersboard_data[1:], start=2):  # Start=2 to account for header row
        if row[nickname_index - 1] == nickname:  # -1 to convert back from Google Sheets indexing
            player_row = i
            break

    if player_row:
        # Player exists, update their record
        cell = leadersboard_data_sheet.cell(player_row, total_index)
        leadersboard_data_sheet.update_cell(player_row, total_index, int(cell.value) + 1)
        if result == 'Win':
            cell = leadersboard_data_sheet.cell(player_row, win_index)
            leadersboard_data_sheet.update_cell(player_row, win_index, int(cell.value) + 1)
        elif result == 'Lose':
            cell = leadersboard_data_sheet.cell(player_row, lose_index)
            leadersboard_data_sheet.update_cell(player_row, lose_index, int(cell.value) + 1)
        elif result == 'Draw':
            cell = leadersboard_data_sheet.cell(player_row, draws_index)
            leadersboard_data_sheet.update_cell(player_row, draws_index, int(cell.value) + 1)
    else:
        # Player doesn't exist, append a new row
        new_row_values = [''] * len(headers)
        new_row_values[nickname_index - 1] = nickname
        new_row_values[total_index - 1] = 1
        new_row_values[win_index - 1] = 1 if result == 'Win' else 0
        new_row_values[lose_index - 1] = 1 if result == 'Lose' else 0
        new_row_values[draws_index - 1] = 1 if result == 'Draw' else 0
        leadersboard_data_sheet.append_row(new_row_values)

def save_board_to_google_sheets(worksheet, board, move):
    board_str = "".join(["X" if cell == 1 else "O" if cell == -1 else " " for row in board for cell in row])
    data_to_insert = [[board_str, move]]
    worksheet.insert_rows(data_to_insert, 2)

def check_game_status(board):
    # Check for a win for each player
    for player in [1, -1]:
        winning_positions = [
            # Horizontal
            board[0], board[1], board[2],
            # Vertical
            [board[0][0], board[1][0], board[2][0]],
            [board[0][1], board[1][1], board[2][1]],
            [board[0][2], board[1][2], board[2][2]],
            # Diagonals
            [board[0][0], board[1][1], board[2][2]],
            [board[0][2], board[1][1], board[2][0]]
        ]
        
        if any(all(pos == player for pos in win_pos) for win_pos in winning_positions):
            return True, player  # A win is detected and return the player who won

    # Check for a draw (all cells are filled)
    if all(cell != 0 for row in board for cell in row):
        return True, 0  # The game is a draw
    
    # If no win or draw, the game is not over
    return False, None