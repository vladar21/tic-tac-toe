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
print(f'use tensorflow version {tf.__version__}')

# Google Drive
from googleapiclient.discovery import build
import io
from googleapiclient.http import MediaIoBaseUpload
from googleapiclient.http import MediaIoBaseDownload
import h5py

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

# Authorize the credentials and create a client using gspread.
CLIENT = gspread.authorize(CREDENTIALS)

SERVICE = build('drive', 'v3', credentials=CREDENTIALS)
MODEL_NAME = "tic_tac_toe_model.h5"

def share_file_with_user(file_id, user_email):
    user_permission = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': user_email
    }
    SERVICE.permissions().create(
        fileId=file_id,
        body=user_permission,
        fields='id',
    ).execute()

def save_model_to_google_drive(model):

    # Serializing a Keras model in h5 format into memory
    model_buffer = io.BytesIO()
    
    # Save the model in HDF5 format to the buffer
    with h5py.File(model_buffer, 'w') as h5file:
        tf.keras.models.save_model(model, h5file)
    model_buffer.seek(0)  # Move the pointer to the beginning of the stream

    # Set metadata for a file that will be uploaded to Google Drive
    file_metadata = {
        'name': MODEL_NAME,
        'mimeType': 'application/octet-stream',  # MIME type for .h5 file
        'parents': '1MgctFDUGBgx2E-ZZac9V71MFAKj-cTqD'  # Adding a Folder ID (TicTacToe folder)
    }
    
    # Preparing a streaming download
    media = MediaIoBaseUpload(model_buffer,
                              mimetype='application/octet-stream',
                              resumable=True)
    
    # Uploading a file to Google Drive
    file = SERVICE.files().create(body=file_metadata,
                                  media_body=media,
                                  fields='id').execute()
    
    print(f'Model {MODEL_NAME} ID: {file.get("id")} success updated')
    print()

def get_model_id_by_name():
    results = SERVICE.files().list(
        q=f"name='{MODEL_NAME}'",
        pageSize=10,
        fields="files(id, name)"
    ).execute()
    items = results.get('files', [])

    if not items:
        print(f"No files with name {MODEL_NAME} found.")
        return None
    else:
        # If several files with the same name are found, we return the ID of the first
        model_id = items[0]['id']
        print()
        print(f"Found model {MODEL_NAME} with ID: {model_id}")
        return model_id

def download_model_from_google_drive(file_id):
    request = SERVICE.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    fh.seek(0)
    
    # Load the Keras model from the h5py File object that is created from the buffer
    with h5py.File(fh, 'r') as h5file:
        model = tf.keras.models.load_model(h5file, compile=False)

        # Compiling the model specifying the optimizer, loss function, and metrics
        model.compile(
            optimizer='adam',              # Optimizer
            loss='sparse_categorical_crossentropy',  # Loss function
            metrics=['accuracy']           # Metrics to track
        )
    
    return model

def load_data_from_google_sheets():
    # Try to open the spreadsheet and the worksheets within it.
    try:
        sheet = CLIENT.open('tic_tac_toe')
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