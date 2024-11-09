import random

def create_grid():
    return [[' ' for _ in range(3)] for _ in range(3)]

def print_grid(grid):
    for i, row in enumerate(grid):
        print('|'.join(row))
        if i < len(grid) - 1:
            print('-' * 5)

def player_chooses_symbol():
    symbol = input("Choose X or O: ").upper()
    while symbol not in ['X', 'O']:
        symbol = input("Invalid choice. Choose X or O: ").upper()
    return symbol

def player_moves(grid, symbol):
    while True:
        try:
            row, col = map(int, input(f"Enter your move (row and column, 1-3): ").split())
            if 1 <= row <= 3 and 1 <= col <= 3 and grid[row-1][col-1] == ' ':
                grid[row-1][col-1] = symbol
                break
            else:
                print("Invalid move. Try again.")
        except ValueError:
            print("Invalid input. Enter two numbers.")

def two_player_moves(grid, symbol):
    print_grid(grid)
    player_moves(grid, symbol)

def player_goes_first():
    return random.choice([True, False])

def computer_moves(grid, symbol, difficulty):
    if difficulty == 'Easy':
        random_move(grid, symbol)
    elif difficulty == 'Normal':
        block_or_random_move(grid, symbol)
    elif difficulty == 'Hard':
        hard_move(grid, symbol)

def random_move(grid, symbol):
    empty_spaces = [(i, j) for i in range(3) for j in range(3) if grid[i][j] == ' ']
    if empty_spaces:
        row, col = random.choice(empty_spaces)
        grid[row][col] = symbol

def block_or_random_move(grid, symbol):
    for i in range(3):
        for j in range(3):
            if grid[i][j] == ' ' and is_winning_move(grid, i, j, symbol):
                grid[i][j] = symbol
                return
    
    random_move(grid, symbol)

def hard_move(grid, symbol):
    def check_win(board, player):
        for i in range(3):
            if all(board[i][j] == player for j in range(3)) or all(board[j][i] == player for j in range(3)):
                return True

        if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
            return True

        return False

    def minimax(board, depth, is_maximizing, alpha, beta):
        if check_win(board, symbol):
            return 1
        elif check_win(board, get_opponent_symbol()):
            return -1
        elif check_for_tie(board):
            return 0

        if is_maximizing:
            max_eval = float('-inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == ' ':
                        board[i][j] = symbol
                        eval = minimax(board, depth + 1, False, alpha, beta)
                        board[i][j] = ' '
                        max_eval = max(max_eval, eval)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
            return max_eval
        else:
            min_eval = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == ' ':
                        board[i][j] = get_opponent_symbol()
                        eval = minimax(board, depth + 1, True, alpha, beta)
                        board[i][j] = ' '
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
            return min_eval

    def get_opponent_symbol():
        return 'O' if symbol == 'X' else 'X'

    best_move = None
    best_eval = float('-inf')
    alpha = float('-inf')
    beta = float('inf')

    for i in range(3):
        for j in range(3):
            if grid[i][j] == ' ':
                grid[i][j] = symbol
                eval = minimax(grid, 0, False, alpha, beta)
                grid[i][j] = ' '
                if eval > best_eval:
                    best_eval = eval
                    best_move = (i, j)

    row, col = best_move
    grid[row][col] = symbol

def is_winning_move(grid, row, col, symbol):
    return (check_row(grid, row, symbol) or
            check_column(grid, col, symbol) or
            check_diagonals(grid, symbol))

def check_row(grid, row, symbol):
    return all(grid[row][col] == symbol for col in range(3))

def check_column(grid, col, symbol):
    return all(grid[row][col] == symbol for row in range(3))

def check_diagonals(grid, symbol):
    return (all(grid[i][i] == symbol for i in range(3)) or
            all(grid[i][2-i] == symbol for i in range(3)))

def check_for_winner(grid):
    for i in range(3):
        if grid[i][0] == grid[i][1] == grid[i][2] != ' ':
            return True
        if grid[0][i] == grid[1][i] == grid[2][i] != ' ':
            return True
    if grid[0][0] == grid[1][1] == grid[2][2] != ' ' or grid[0][2] == grid[1][1] == grid[2][0] != ' ':
        return True
    return False

def check_for_tie(grid):
    return all(grid[i][j] != ' ' for i in range(3) for j in range(3))

def end_of_match_message(player_symbol, computer_symbol, winner):
    if winner == "Player":
        print("You win!")
    elif winner == "Computer":
        print("You lose!")


def end_of_match_multiplayer(winner):
    if winner == 1:
        print("Player O won!")
    elif winner == 0:
        print("Player X won!")
    else:
        print("Tie!")

def play_again():
    return input("Do you want to play again? (yes/no): ").lower() == 'yes'

def choose_difficulty():
    return input("Choose difficulty (Easy/Normal/Hard): ").capitalize()

def tic_tac_toe():
    print("Hello, Welcome to Tic Tac Toe!")
    
    while True:
        grid = create_grid()
        print_grid(grid)

        gameMode = input("Choose 1 to play against computer, 2 for multiplayer: ")

        #computer 
        if gameMode == '1':
            player_symbol = player_chooses_symbol()
            computer_symbol = 'X' if player_symbol == 'O' else 'O'

            current_player = 'Player 1' if player_goes_first() else 'Player 2'

            if player_goes_first():
                current_player = 'Player'
            else:
                current_player = 'Computer'

            difficulty = choose_difficulty()

            while True:
                print(f"\n{current_player}'s turn:")

                if current_player == 'Player':
                    player_moves(grid, player_symbol)
                else:
                    computer_moves(grid, computer_symbol, difficulty)

                print_grid(grid)

                if check_for_winner(grid):
                    end_of_match_message(player_symbol, computer_symbol, current_player)
                    break
                elif check_for_tie(grid):
                    print("Tie!")
                    break

                current_player = 'Player' if current_player == 'Computer' else 'Computer'

        #multiplayer
        elif gameMode == '2':
            player = ['X','O']
            currentPlayer = 0
            
            while True:
                print(f"Player {player[currentPlayer]}'s turn.")
                two_player_moves(grid, player[currentPlayer])

                if check_for_winner(grid):
                    end_of_match_multiplayer(currentPlayer)
                    break
                elif check_for_tie(grid):
                    print("Tie!")
                    break
                
                currentPlayer = (currentPlayer + 1) % 2
        
        if not play_again():
            print("Thank you for playing!")
            break

tic_tac_toe()
