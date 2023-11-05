# work with warnings
import warnings
# Suppress all UserWarnings
warnings.filterwarnings('ignore', category=UserWarning)

# Google Sheet
# import gspread
# from google.oauth2.service_account import Credentials
# work with filesystem
import os
# AI model
import tensorflow as tf
print(f'tensorflow version {tf.__version__}')
from tensorflow import keras
# my library
from tic_tac_toe_ui import display_start_game, display_board, display_leadersboard
from tic_tac_toe_google import save_model_to_google_drive, get_model_id_by_name, download_model_from_google_drive, load_data_from_google_sheets, update_leadersboard, save_board_to_google_sheets
# Google Drive
# from googleapiclient.discovery import build
# import io
# from googleapiclient.http import MediaIoBaseUpload
# from googleapiclient.http import MediaIoBaseDownload
# import h5py

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# SERVICE_ACCOUNT_FILE = 'creds.json'
# SCOPES = [
#     'https://www.googleapis.com/auth/drive',
#     "https://www.googleapis.com/auth/spreadsheets",
#     "https://www.googleapis.com/auth/drive.file"
# ]

# CREDENTIALS = Credentials.from_service_account_file(
#     SERVICE_ACCOUNT_FILE,
#     scopes=SCOPES
# )

# # Authorize the credentials and create a client using gspread.
# CLIENT = gspread.authorize(CREDENTIALS)

# SERVICE = build('drive', 'v3', credentials=CREDENTIALS)
# MODEL_NAME = "tic_tac_toe_model.h5"


#################################################################
############## work with TensorFlow model #######################

def load_or_train_model(worksheet):
    try:
        file_id = get_model_id_by_name()
        if file_id == None:
            return train_model(worksheet)
        # Trying to download a model from Google Drive
        model = download_model_from_google_drive(file_id)
        print("Model loaded successfully from Google Drive.")
    except Exception as e:
        print(f"An error occurred while loading the model from Google Drive: {e}")
        # Here's the code to train the model if loading fails...
        return train_model(worksheet)
    
    return model


def train_model(worksheet):
    data = worksheet.get_all_values()
    if not data:
        print("The worksheet is empty. Starting with empty data.")
        return None  # Explicitly return None

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

        model.fit(X_train, y_train, epochs=50, verbose=0)
        return model
    else:
        print("No training data available. Starting with an untrained model.")
        return None
    
############## work with TensorFlow model #######################
#################################################################

###########################################
############## game #######################

def player_turn(board, X_train, y_train, tic_tac_toe_data_sheet):
    try:
        move = int(input("Your move (0-8): \n"))
        if board[move // 3][move % 3] != 0:
            print("Cell is already taken. Please choose another cell.")
            return False  # Turn was not successful.
        board[move // 3][move % 3] = 1
        flattened_board = [cell for row in board for cell in row]
        X_train.append(flattened_board)
        y_train.append(move)
        save_board_to_google_sheets(tic_tac_toe_data_sheet, board, move)
        return True  # Turn was successful.
    except (ValueError, IndexError):
        print("Invalid input. Please enter a number from 0 to 8.")
        return False  # Turn was not successful.

def ai_turn(board, model, X_train, tic_tac_toe_data_sheet):
    flattened_board = [cell for row in board for cell in row]
    board_as_input = [flattened_board]
    prediction = model.predict(board_as_input)[0]
    valid_moves = [i for i in range(9) if board[i // 3][i % 3] == 0]
    best_move = max(valid_moves, key=lambda i: prediction[i])
    board[best_move // 3][best_move % 3] = -1
    flattened_board = [cell for row in board for cell in row]
    X_train.append(flattened_board)
    save_board_to_google_sheets(tic_tac_toe_data_sheet, board, best_move)

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

def check_and_handle_game_over(board, leadersboard_data_sheet, nickname):
    game_over, winner = check_game_status(board)
    if game_over:
        if winner == 1:
            print("Player X wins!")
            result = "Win"
        elif winner == -1:
            print("Player O wins!")
            result = "Lose"
        else:
            print("The game is a draw!")
            result = "Draw"
        update_leadersboard(leadersboard_data_sheet, nickname, result)
        return True  # The game is over.
    return False  # The game is not over.

def prompt_replay():
    print("\nPlay again?")
    play_or_no = input("(Y - if yes, any other - if no): \n").lower()
    return play_or_no == 'y'

def game(leadersboard_data_sheet, tic_tac_toe_data_sheet, nickname):
    print('\nGame starting.\n')
    display_start_game()
    current_player = 1
    board = [[0, 0, 0] for _ in range(3)]
    X_train = []  # Initialisation of the list for storing board states
    y_train = []  # Initialising the list for storing moves
    model = load_or_train_model(tic_tac_toe_data_sheet)
    
    while True:
        if current_player == 1:
            if not player_turn(board, X_train, y_train, tic_tac_toe_data_sheet):
                continue  # Player needs to retry their turn.
        else:
            ai_turn(board, model, X_train, tic_tac_toe_data_sheet)
        
        display_board(board)

        if check_and_handle_game_over(board, leadersboard_data_sheet, nickname):
            if not prompt_replay():
                display_leadersboard(leadersboard_data_sheet)
                break  # Exit the game loop.
            board = [[0, 0, 0] for _ in range(3)]  # Reset the board.
        
        current_player = -current_player  # Switch players.

    if model is not None:
        save_model_to_google_drive(model)

############## game #######################
###########################################


def main():
    # Load data from Google Sheets at the start of the main function
    leadersboard_data_sheet, tic_tac_toe_data_sheet = load_data_from_google_sheets()

    if not leadersboard_data_sheet or not tic_tac_toe_data_sheet:
        print("Error loading data from Google Sheets.")
        return  # Exit the function if data loading was unsuccessful

    # Main game loop
    
    print("\nTic Tac Toe with Ai")
    print()
    nickname = input("Please enter your nickname (it must be unique): \n").strip()

    start = str(input("Do you want to play game, exit or look at the leadersboard? \n(Y - game, L - leadersboar, any other - exit): \n"))
    start = start.lower()
    # Main game loop
    if start == 'y':
        game(leadersboard_data_sheet, tic_tac_toe_data_sheet, nickname)
    elif start == 'l':
        display_leadersboard(leadersboard_data_sheet)
        start = str(input("Do you want to play game or exit? \n(Y - game, any other - exit): \n"))
        start = start.lower()
        if start == 'y':
            game(leadersboard_data_sheet, tic_tac_toe_data_sheet, nickname)
        else:
            print("\nGame over.\n")
    else:
        print("\nGame over.\n")
        
# Ensure that the main function is called when the script is executed
if __name__ == "__main__":
    main()