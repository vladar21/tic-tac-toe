# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

# Start board
def display_start_board():
    print("\nWelcome to the good old game of Tic-Tac-Toe in a modern interpretation.\n")
    print("Your opponent will be a self-learning artificial intelligence.\n")
    start_board = ['0', '1', '2', '3', '4', '5', '6', '7', '8']
    print(f" {start_board[0]} | {start_board[1]} | {start_board[2]} ")
    print(" --------- ")
    print(f" {start_board[3]} | {start_board[4]} | {start_board[5]} ")
    print(" --------- ")
    print(f" {start_board[6]} | {start_board[7]} | {start_board[8]} ")

def main():
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