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
def display_start_board():
    print("\nTic Tac Toe with Ai")
    print()
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

import gspread
from google.oauth2.service_account import Credentials

import gspread
from google.oauth2.service_account import Credentials

def update_leaderboards(leaderboard_sheet, human_nickname, win_human, win_ai):
   
    leaderboard_old_data = leaderboard_sheet.get_all_values()

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

        leaderboard_sheet.update(f'C{row_index+2}', [[win_human]])
        leaderboard_sheet.update(f'D{row_index+2}', [[win_ai]])
        leaderboard_sheet.update(f'B{row_index+2}', [[total_games]])
    else:
        # Create a new row with the given values
        new_row = [human_nickname, 1, win_human, win_ai]
        leaderboard_sheet.append_table(new_row)



    

def save_board_to_google_sheets(board, move):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = Credentials.from_service_account_file('creds.json', scopes=scope)
    gc = gspread.authorize(creds)

    spreadsheet = gc.open_by_key('1N2eosTHbj1OdRRdJkLrf2IKxIXOp1k80wb2kht6caJc')
    worksheet = spreadsheet.worksheet('cross_zerro')

    board_str = "".join(["X" if cell == 1 else "O" if cell == -1 else " " for row in board for cell in row])
    data_to_insert = [[board_str, move]]
    worksheet.insert_rows(data_to_insert, 2)

def main():
    # Main game loop
    current_player = 1
    # Display start board
    display_start_board()
    start = str(input("\nLet `s start? \n(Yes - y or Y, No - any other)\n"))
    if start.lower() == 'y':
        print('\nGame starting.\n')
        while True:  
            print("starting while true cicle")
            break
    else:
        print("\nGame over.\n")
        
main()