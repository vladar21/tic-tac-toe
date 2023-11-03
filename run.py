import gspread
from google.oauth2.service_account import Credentials
import os
import tensorflow as tf
from tensorflow import keras
from funcs import display_start_game

tf.data.experimental.enable_debug_mode()
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def check_model_availability():

    model_directory = 'tic_tac_toe_model'
    model_file = os.path.join(model_directory, 'saved_model.pb')  # Assuming saved_model.pb is the model file
    if not os.path.exists(model_file):
        print("Model file 'saved_model.pb' does not exist.")
        return False
    try:
        # Attempt to load the model to ensure it's not only present but also loadable
        keras.models.load_model(model_directory)  # In TensorFlow 2.x, you load the whole directory
    except Exception as e:
        print(f"An error occurred while loading the model: {e}")
        return False
    return True

def load_or_train_model(worksheet):
    model_directory = 'tic_tac_toe_model'
    model_file = os.path.join(model_directory, 'tic_tac_toe_model.h5')
    
    if os.path.exists(model_file):
        model = keras.models.load_model(model_file)
    else:
        data = worksheet.get_all_values()

        if not data:
            print("The worksheet is empty. Starting with empty data.")
            return [], []

        X_train = []
        y_train = []

        for row in data:
            if len(row) < 2 or not row[0]:
                continue

            board_state = [1 if cell == 'X' else -1 if cell == 'O' else 0 for cell in row[0]]
            X_train.append(board_state)
            move = int(row[1])
            y_train.append(move)

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
            model = None
    return model

def load_data_from_google_sheets():

    # Define the scope of the access.
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"
    ]

    # Checking file availability creds.json
    creds_file = 'creds.json'
    if not os.path.exists(creds_file):
        print("Credentials file 'creds.json' not found.")
        return None, None, None
    if not os.access(creds_file, os.R_OK):
        print("Credentials file 'creds.json' is not readable.")
        return None, None, None

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

    return leadersboard_data_sheet, tic_tac_toe_data_sheet
    
def display_leadersboard(leadersboard_data_sheet):

    # Fetching the data from the sheet
    leadersboard_data = leadersboard_data_sheet.get_all_values()
    
    print("\nLeadersboard")

    # Headers for the table
    headers = ["PP", "Human Nickname", "Win Human", "Win AI", "Draw"]  # Added "Draw" to headers

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
    nickname_index = headers.index("Human Nickname") + 1  # +1 for Google Sheets indexing
    win_index = headers.index("Win Human") + 1
    lose_index = headers.index("Win AI") + 1
    draw_index = headers.index("Draw") + 1

    # Find the player in the leaderboard
    player_row = None
    for i, row in enumerate(leadersboard_data[1:], start=2):  # Start=2 to account for header row
        if row[nickname_index - 1] == nickname:  # -1 to convert back from Google Sheets indexing
            player_row = i
            break

    if player_row:
        # Player exists, update their record
        if result == 'Win':
            cell = leadersboard_data_sheet.cell(player_row, win_index)
            leadersboard_data_sheet.update_cell(player_row, win_index, int(cell.value) + 1)
        elif result == 'Lose':
            cell = leadersboard_data_sheet.cell(player_row, lose_index)
            leadersboard_data_sheet.update_cell(player_row, lose_index, int(cell.value) + 1)
        elif result == 'Draw':
            cell = leadersboard_data_sheet.cell(player_row, draw_index)
            leadersboard_data_sheet.update_cell(player_row, draw_index, int(cell.value) + 1)
    else:
        # Player doesn't exist, append a new row
        new_row_values = [''] * len(headers)
        new_row_values[nickname_index - 1] = nickname
        new_row_values[win_index - 1] = 1 if result == 'Win' else 0
        new_row_values[lose_index - 1] = 1 if result == 'Lose' else 0
        new_row_values[draw_index - 1] = 1 if result == 'Draw' else 0
        leadersboard_data_sheet.append_row(new_row_values)

def save_board_to_google_sheets(worksheet, board, move):
    board_str = "".join(["X" if cell == 1 else "O" if cell == -1 else " " for row in board for cell in row])
    data_to_insert = [[board_str, move]]
    worksheet.insert_rows(data_to_insert, 2)

def is_game_over(board):

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

def main():
    check_model_availability()

    # Load data from Google Sheets at the start of the main function
    leadersboard_data_sheet, tic_tac_toe_data_sheet = load_data_from_google_sheets()

    if not leadersboard_data_sheet or not tic_tac_toe_data_sheet:
        print("Error loading data from Google Sheets.")
        return  # Exit the function if data loading was unsuccessful

    # Main game loop
    
    print("\nTic Tac Toe with Ai")
    print()
    nickname = input("Please enter your nickname (it must be unique): ").strip()

    start = str(input("Do you want to play game, exit or look at the leadersboard? \n(Y - game, L - leadersboar, any other - exit): "))
    start = start.lower()
    # Main game loop
    if start == 'y':
        print('\nGame starting.\n')
        display_start_game()
        current_player = 1
        X_train = []
        y_train = []
        board = [[0, 0, 0] for _ in range(3)]  # Initialize the board.
        model = load_or_train_model(tic_tac_toe_data_sheet)
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
                    # Save the current board state to Google Sheets
                    save_board_to_google_sheets(tic_tac_toe_data_sheet, board, move)
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
                    # Save the current board state to Google Sheets
                    save_board_to_google_sheets(tic_tac_toe_data_sheet, board, best_move)
            display_board(board)
            current_player = 1 if current_player == -1 else -1
        if model is not None:
           model_directory = 'tic_tac_toe_model'
           model_file = os.path.join(model_directory, 'tic_tac_toe_model.keras')
           model.save(model_file)
    elif start == 'l':
        display_leadersboard(leadersboard_data_sheet)
    else:
        print("\nGame over.\n")
        
# Ensure that the main function is called when the script is executed
if __name__ == "__main__":
    main()