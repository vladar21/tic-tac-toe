# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

import gspread
from google.oauth2.service_account import Credentials
import os
import tensorflow as tf
from tensorflow import keras

tf.data.experimental.enable_debug_mode()
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def load_data_from_google_sheets():
    """
    Initialize the Google Sheets client, open the spreadsheet, and load data sheets.

    This function uses the credentials file 'creds.json' to authorize access to Google Sheets
    and opens a spreadsheet titled 'tic_tac_toe' to retrieve two specific worksheets within it.
    It also initializes the game board with zeros, representing an empty board.

    Returns:
        tuple: A tuple containing the leaderboard worksheet, tic_tac_toe_data_sheet worksheet, and the initial board state.
        Returns None for each if an exception occurs during the process.
    """
    # Define the scope of the access.
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"
    ]

    # Load the credentials from the 'creds.json' file.
    try:
        creds = Credentials.from_service_account_file('creds.json', scopes=scope)
    except FileNotFoundError:
        print("Credentials file 'creds.json' not found.")
        return None, None, None
    except Exception as e:
        print(f"An error occurred while loading credentials: {e}")
        return None, None, None

    # Authorize the credentials and create a client using gspread.
    client = gspread.authorize(creds)

    # Try to open the spreadsheet and the worksheets within it.
    try:
        sheet = client.open('tic_tac_toe')
        leadersboard_data_sheet = sheet.worksheet('leadersboard')
        tic_tac_toe_data_sheet = sheet.worksheet('tic_tac_toe_data_sheet')
    except gspread.exceptions.SpreadsheetNotFound:
        print("The spreadsheet 'tic_tac_toe' was not found.")
        return None, None, None
    except gspread.exceptions.WorksheetNotFound:
        print("A required worksheet was not found in the spreadsheet.")
        return None, None, None
    except Exception as e:
        print(f"An error occurred while opening the spreadsheet: {e}")
        return None, None, None

    # Initialize the board.
    board = [[0, 0, 0] for _ in range(3)]

    return leadersboard_data_sheet, tic_tac_toe_data_sheet, board


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
    """
    Print the Tic-Tac-Toe board to the console.

    Args:
    board (list of list of int): The game board, a 3x3 list.
                                  Each cell contains 0 (empty), 1 (player 1's 'X'), or -1 (player 2's 'O').
    """
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

def work_with_model():
    model_directory = 'tic_tac_toe_model'
    model_file = os.path.join(model_directory, 'tic_tac_toe_model.keras')
    if os.path.exists(model_file):
        model = keras.models.load_model(model_file)
    else:
        X_train, y_train = load_data_from_google_sheets()

        if len(X_train) > 0:
            model = keras.Sequential([
                keras.layers.Input(shape=(9,)),
                keras.layers.Dense(128, activation='relu'),
                keras.layers.Dense(9, activation='softmax')
            ])

            model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

            model.fit(X_train, y_train, epochs=50)
        else:
            print("No training data available. Starting with an untrained model.")
            X_train = []
            y_train = []
            model = None
    return model

def main():
    # Load data from Google Sheets at the start of the main function
    leadersboard_data_sheet, tic_tac_toe_data_sheet, board = load_data_from_google_sheets()

    if not leadersboard_data_sheet or not tic_tac_toe_data_sheet:
        print("Error loading data from Google Sheets.")
        return  # Exit the function if data loading was unsuccessful

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
        model = work_with_model()
        while True:           
            if is_game_over(board):
                print("Game over.")
                display_board(board)
                break
            if current_player == 1:
                move = int(input("Your move (0-8): "))
                if board[move // 3][move % 3] == 0:
                    board[move // 3][move % 3] = 1
                    flattened_board = [cell for row in board for cell in row]
                    X_train.append(flattened_board)
                    y_train.append(move)
            else:
                if model is not None:
                    flattened_board = [cell for row in board for cell in row]
                    board_as_input = [flattened_board]
                    prediction = model.predict(board_as_input)[0]
                    valid_moves = [i for i in range(9) if board[i // 3][i % 3] == 0]
                    best_move = max(valid_moves, key=lambda i: prediction[i])
                    board[best_move // 3][best_move % 3] = -1
                    flattened_board = [cell for row in board for cell in row]
                    X_train.append(flattened_board)
            display_board(board)
            current_player = 1 if current_player == -1 else -1
        if model is not None:
           model.save(model_file)
    elif start == 'l':
        display_leadersboard(leadersboard_data_sheet)
    else:
        print("\nGame over.\n")
        
# Ensure that the main function is called when the script is executed
if __name__ == "__main__":
    main()