# work with warnings
import warnings
# Suppress all UserWarnings
warnings.filterwarnings('ignore', category=UserWarning)

# Google Sheet
import gspread
from google.oauth2.service_account import Credentials
# work with filesystem
import os
# AI model
import tensorflow as tf
from tensorflow import keras
# my library
from funcs import display_start_game, display_board, display_leadersboard, update_leadersboard, save_board_to_google_sheets, check_game_status
# Google Drive
from googleapiclient.discovery import build
import io
from googleapiclient.http import MediaIoBaseUpload
from googleapiclient.http import MediaIoBaseDownload
import h5py
from keras.models import load_model


# tf.data.experimental.enable_debug_mode()
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


SERVICE_ACCOUNT_FILE = 'creds.json'
SCOPES = [
    'https://www.googleapis.com/auth/drive',
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file"
]

CREDENTIALS = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=SCOPES
)

SERVICE = build('drive', 'v3', credentials=CREDENTIALS)
MODEL_NAME = "tic_tac_toe_model.h5"


def share_file_with_user(service, file_id, user_email):
    user_permission = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': user_email
    }
    service.permissions().create(
        fileId=file_id,
        body=user_permission,
        fields='id',
    ).execute()


def save_model_to_google_drive(service, model, model_name):

    results = service.files().list(
        q="'1MgctFDUGBgx2E-ZZac9V71MFAKj-cTqD' in parents",
        pageSize=10,
        fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))


    # Serializing a Keras model in h5 format into memory
    model_buffer = io.BytesIO()
    
    # Save the model in HDF5 format to the buffer
    with h5py.File(model_buffer, 'w') as h5file:
        tf.keras.models.save_model(model, h5file)
    model_buffer.seek(0)  # Move the pointer to the beginning of the stream

    # Set metadata for a file that will be uploaded to Google Drive
    file_metadata = {
        'name': model_name,
        'mimeType': 'application/octet-stream',  # MIME type for .h5 file
        'parents': '1MgctFDUGBgx2E-ZZac9V71MFAKj-cTqD'  # Adding a Folder ID (TicTacToe folder)
    }
    
    # Preparing a streaming download
    media = MediaIoBaseUpload(model_buffer,
                              mimetype='application/octet-stream',
                              resumable=True)
    
    # Uploading a file to Google Drive
    file = service.files().create(body=file_metadata,
                                  media_body=media,
                                  fields='id').execute()
    
    print(f'Model {model_name} ID: {file.get("id")}')

    share_file_with_user(service, "1-kaiGuc_BDqXknwHBSH1ZBK_hrc3WBkq", 'vladar21@gmail.com')

def get_model_id_by_name(service, model_name):
    results = service.files().list(
        q=f"name='{model_name}'",
        pageSize=10,
        fields="files(id, name)"
    ).execute()
    items = results.get('files', [])

    if not items:
        print(f"No files with name {model_name} found.")
        return None
    else:
        # If several files with the same name are found, we return the ID of the first
        model_id = items[0]['id']
        print(f"Found model {model_name} with ID: {model_id}")
        return model_id

def download_model_from_google_drive(service, file_id):
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    fh.seek(0)
    
    # Load the Keras model from the h5py File object that is created from the buffer
    with h5py.File(fh, 'r') as h5file:
        model = tf.keras.models.load_model(h5file)
    
    return model

def load_or_train_model(service, model_name, worksheet):
    try:
        file_id = get_model_id_by_name(service, model_name)
        if file_id == None:
            return train_model(worksheet)
        # Trying to download a model from Google Drive
        model = download_model_from_google_drive(service, file_id)
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
    
def game(service, model_name, leadersboard_data_sheet, tic_tac_toe_data_sheet, nickname):
    print('\nGame starting.\n')
    display_start_game()
    current_player = 1
    X_train = []
    y_train = []
    board = [[0, 0, 0] for _ in range(3)]  # Initialize the board.
    model = load_or_train_model(service, model_name, tic_tac_toe_data_sheet)
    while True:           
        game_over, winner = check_game_status(board)
        if game_over:
            if winner == 1:
                print("Player X wins!")
                result = "Win"
            elif winner == -1:
                print("Player O wins!")
                result = "Lose"
            elif winner == 0:
                print("The game is a draw!")
                result = "Draw"
            update_leadersboard(leadersboard_data_sheet, nickname, result)
            print("\nPlay again?")
            play_or_no = str(input("(Y - if yes, any other - if no): \n"))
            play_or_no = play_or_no.lower()
            board = [[0, 0, 0] for _ in range(3)]
            if play_or_no != 'y':
                display_leadersboard(leadersboard_data_sheet)
                break
        if current_player == 1:
            move = int(input("Your move (0-8): \n"))
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
        # save model to the Google Drive
        save_model_to_google_drive(SERVICE, model, MODEL_NAME)
        

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
        game(SERVICE, MODEL_NAME, leadersboard_data_sheet, tic_tac_toe_data_sheet, nickname)
    elif start == 'l':
        display_leadersboard(leadersboard_data_sheet)
        start = str(input("Do you want to play game or exit? \n(Y - game, any other - exit): \n"))
        start = start.lower()
        if start == 'y':
            game(SERVICE, MODEL_NAME, leadersboard_data_sheet, tic_tac_toe_data_sheet, nickname)
        else:
            print("\nGame over.\n")
    else:
        print("\nGame over.\n")
        
# Ensure that the main function is called when the script is executed
if __name__ == "__main__":
    main()