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
leadersboard_sheet = SHEET.worksheet('leadersboard')
tic_tac_toe_data_sheet = SHEET.worksheet('tic_tac_toe_data_sheet')

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

def display_leadersboard():
    print()
    input("Do you want to play game or look at the leadersboard? (Y - game, any other - look at)")

def update_leadersboard(leadersboard_sheet, human_nickname, win_human, win_ai):
    """
    Update leadersboard data on the Google Sheet
    """
    leaderboard_old_data = leadersboard_sheet.get_all_values()

    # Find the row index for the given human_nickname, if it exists
    row_index = None
    for i, row in enumerate(leaderboard_old_data):
        if row[0] == human_nickname:
            row_index = i
            break

    # If the human_nickname exists, update the row; otherwise, add a new row
    if row_index is not None:
        # Update win_human, win_ai, and total_games
        win_human = int(row[2]) + win_human
        win_ai = int(row[3]) + win_ai
        total_games = int(row[1]) + 1

        leadersboard_sheet.update(f'C{row_index+2}', [[win_human]])
        leadersboard_sheet.update(f'D{row_index+2}', [[win_ai]])
        leadersboard_sheet.update(f'B{row_index+2}', [[total_games]])
    else:
        # Create a new row with the given values
        new_row = [human_nickname, 1, win_human, win_ai]
        leadersboard_sheet.append_row(new_row)

def main():
    # Main game loop
    current_player = 1
    print("\nTic Tac Toe with Ai")
    print()
    start = str(input("Do you want to play game, exit or look at the leadersboard? \n(Y - game, L - leadersboar, any other - exit): "))
    start = start.lower()
    # Main game loop
    if start == 'y':
        print('\nGame starting.\n')
        while True:  
            print("starting while true cicle")
            break
    elif start == 'l':
        display_start_game()
    else:
        print("\nGame over.\n")
        
main()