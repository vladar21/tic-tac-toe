# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('tic_tac_toe')
leadersboard_data_sheet = SHEET.worksheet('leadersboard')
tic_tac_toe_data_sheet = SHEET.worksheet('tic_tac_toe_data_sheet')
board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

# Start board
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

def display_leadersboard(leadersboard_data_sheet):
    """
    Fetch and display the leaderboard from a Google Sheets document in a formatted table.

    Parameters:
    leadersboard_data_sheet: A worksheet object containing the leaderboard data, where each row contains 
                             the details of a leader. The details include human nickname, number of wins by the human,
                             and number of wins by the AI.
    """
    # Fetching the data from the sheet
    leadersboard_data = leadersboard_data_sheet.get_all_values()
    
    print("\nLeadersboard")

    # Headers for the table
    headers = ["PP", "Human Nickname", "Win Human", "Win AI"]

    # Find the maximum length of data in each column for proper spacing
    column_lengths = [len(header) for header in headers]
    for row in leadersboard_data:
        for i, cell in enumerate(row):
            column_lengths[i] = max(column_lengths[i], len(cell))

    # Adding 'PP' column which is not in the Google Sheet
    leadersboard_data.insert(0, headers)
    column_lengths.insert(0, len(headers[0]))  # Assuming 'PP' length is less than header 'PP'

    # Creating the format string for each row
    row_format = " | ".join(["{:<" + str(length) + "}" for length in column_lengths])

    # Print the formatted header row
    print(row_format.format(*leadersboard_data[0]))
    print("-" * (sum(column_lengths) + 3 * (len(headers) - 1)))  # Print header separator

    # Print the formatted data rows
    for index, row in enumerate(leadersboard_data[1:], start=1):  # We skip the header row which is now the first item in the list
        print(row_format.format(index, *row))
    
def display_leadersboard(leadersboard_data_sheet):
    """
    Fetch and display the leaderboard from a Google Sheets document in a formatted table.

    Parameters:
    leadersboard_data_sheet: A worksheet object containing the leaderboard data, where each row contains 
                             the details of a leader, excluding the first row which contains column headers.
    """
    # Fetching the data from the sheet
    leadersboard_data = leadersboard_data_sheet.get_all_values()
    
    print("\nLeadersboard")

    # Headers for the table
    headers = ["PP", "Human Nickname", "Win Human", "Win AI"]

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
    for i in range(1, len(leadersboard_data)):  # Start with 1 to skip header row
        # Get the row data, skipping the header
        row = leadersboard_data[i]
        
        # If the row has less columns than headers, append empty strings
        row += [""] * (len(headers) - len(row))
        print(row_format.format(i, *row))

def is_game_over(board):
    """
    Check if the Tic-Tac-Toe game is over.
    The game is over if there is a winner or if all cells are filled (a draw).

    Args:
    board (list of list of int): The game board represented by a 3x3 list.
    Each cell contains 0 (empty), 1 (player 1), or -1 (player 2).

    Returns:
    bool: True if the game is over, False otherwise.
    """
    # Check for a win for each player
    for player in [1, -1]:
        if (
            any(all(cell == player for cell in row) for row in board) or  # Check rows for a win
            any(all(row[i] == player for row in board) for i in range(3)) or  # Check columns for a win
            all(board[i][i] == player for i in range(3)) or  # Check main diagonal for a win
            all(board[i][2 - i] == player for i in range(3))  # Check secondary diagonal for a win
        ):
            return True  # A win is detected

    # Check for a draw (all cells are filled)
    if all(cell != 0 for row in board for cell in row):
        return True  # The game is a draw

    # If no win or draw, the game is not over
    return False

def display_board(board):
    print()
    for row in board:
        print(" | ".join(["X" if cell == 1 else "O" if cell == -1 else " " for cell in row]))
        print("-" * 9)
    print()

def main():
    # Main game loop
    
    print("\nTic Tac Toe with Ai")
    print()
    start = str(input("Do you want to play game, exit or look at the leadersboard? \n(Y - game, L - leadersboar, any other - exit): "))
    start = start.lower()
    # Main game loop
    if start == 'y':
        print('\nGame starting.\n')
        display_start_game()
        current_player = 1
        X_train = []
        y_train = []
        while True:           
            if is_game_over(board):
                print("Game over.")
                display_board(board)
                break
    elif start == 'l':
        display_leadersboard(leadersboard_data_sheet)
    else:
        print("\nGame over.\n")
        
main()