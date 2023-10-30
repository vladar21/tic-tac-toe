# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

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