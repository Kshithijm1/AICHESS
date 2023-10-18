# Constants for piece values
PIECE_VALUES = {
    'P': 10, 'N': 30, 'B': 30, 'R': 50, 'Q': 90, 'K': 900,
    'p': -10, 'n': -30, 'b': -30, 'r': -50, 'q': -90, 'k': -900
}

# Initial chess board setup
INITIAL_BOARD = [
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
]

# Function to print the chess board
def print_board(board):
    print("   a b c d e f g h")
    for i, row in enumerate(board):
        print(8 - i, " ", end="")
        for piece in row:
            print(piece, end=" ")
        print(8 - i)

# Function to evaluate the current state of the board
def evaluate_board(board):
    score = 0
    for row in board:
        for piece in row:
            score += PIECE_VALUES.get(piece, 0)
    return score

# Function to generate all legal moves for a player
def generate_moves(board, player):
    moves = []
    for r1 in range(8):
        for c1 in range(8):
            piece = board[r1][c1]
            if piece.islower() == player.islower():
                for r2 in range(8):
                    for c2 in range(8):
                        move = ((r1, c1), (r2, c2))
                        if is_valid_move(board, move, player):
                            moves.append(move)
    return moves

# Function to check if a move is valid
def is_valid_move(board, move, player):
    (r1, c1), (r2, c2) = move
    piece = board[r1][c1]

    if piece.islower() == player.islower() and (r1, c1) != (r2, c2):
        if piece == 'p' or piece == 'P':
            if player.islower() and r2 > r1:
                return False
            if not player.islower() and r2 < r1:
                return False

        if piece.lower() == 'p' and (r1 - r2) ** 2 + (c1 - c2) ** 2 > 1:
            return False

        if piece.lower() == 'k' and (abs(r1 - r2) > 1 or abs(c1 - c2) > 1):
            return False

        if piece.lower() == 'n' and (abs(r1 - r2) * abs(c1 - c2) != 2):
            return False

        # Check if moving into check
        board_copy = [row.copy() for row in board]
        make_move(board_copy, move)
        if is_check(board_copy, player):
            return False

    return True

# Function to make the AI's move using minimax with alpha-beta pruning
def make_ai_move(board, depth, player, alpha, beta):
    if depth == 0:
        return evaluate_board(board)

    legal_moves = generate_moves(board, player)
    best_move = None

    if player.islower():
        best_score = float('inf')
        for move in legal_moves:
            board_copy = [row.copy() for row in board]
            make_move(board_copy, move)
            score = make_ai_move(board_copy, depth - 1, player.upper(), alpha, beta)
            if score < best_score:
                best_score = score
                best_move = move
            beta = min(beta, score)
            if beta <= alpha:
                break
    else:
        best_score = -float('inf')
        for move in legal_moves:
            board_copy = [row.copy() for row in board]
            make_move(board_copy, move)
            score = make_ai_move(board_copy, depth - 1, player.lower(), alpha, beta)
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, score)
            if beta <= alpha:
                break

    if best_move:
        make_move(board, best_move)
    return best_score

# Function to check if a king is in check
def is_check(board, player):
    for r1 in range(8):
        for c1 in range(8):
            piece = board[r1][c1]
            if piece.islower() == player.islower():
                for r2 in range(8):
                    for c2 in range(8):
                        if is_valid_move(board, ((r1, c1), (r2, c2)), player):
                            return True
    return False

# Function to make a move on the board
def make_move(board, move):
    from_square, to_square = move
    r1, c1 = from_square
    r2, c2 = to_square

    piece = board[r1][c1]
    board[r2][c2] = piece
    board[r1][c1] = ' '

# Function to promote a pawn
def promote_pawn(board, square, piece):
    r, c = square
    board[r][c] = piece

# Function to play a game with the AI
def play_game_with_ai():
    board = [row.copy() for row in INITIAL_BOARD]
    player_turn = True  # True for player, False for AI
    move_history = []
    move_count = 0
    fifty_move_count = 0

    while True:
        print_board(board)

        if is_check(board, 'w'):
            print("Check!")
            if not generate_moves(board, 'w'):
                print("Checkmate! AI wins.")
                break

        if is_check(board, 'b'):
            print("Check!")
            if not generate_moves(board, 'b'):
                print("Checkmate! Player wins.")
                break

        if not generate_moves(board, 'w') and not is_check(board, 'w'):
            print("Stalemate! It's a draw.")
            break

        if not generate_moves(board, 'b') and not is_check(board, 'b'):
            print("Stalemate! It's a draw.")
            break

        # Check for 50-move rule
        if fifty_move_count >= 50:
            print("Draw due to the 50-move rule.")
            break

        if player_turn:
            # Player's move
            while True:
                move_input = input("Enter your move (e.g., 'e2 e4'): ").split()
                if len(move_input) != 2:
                    print("Invalid move format. Try again.")
                    continue

                from_square = (int(move_input[0][1]) - 1, ord(move_input[0][0]) - ord("a"))
                to_square = (int(move_input[1][1]) - 1, ord(move_input[1][0]) - ord("a"))

                if board[from_square[0]][from_square[1]].islower():
                    print("Invalid piece selection. Try again.")
                    continue

                if not is_valid_move(board, (from_square, to_square), 'w'):
                    print("Invalid move. Try again.")
                    continue

                # Handle castling
                if board[from_square[0]][from_square[1]] == 'K' and from_square == (7, 4) and to_square == (7, 6):
                    board[7][5] = 'R'
                    board[7][7] = ' '
                elif board[from_square[0]][from_square[1]] == 'K' and from_square == (7, 4) and to_square == (7, 2):
                    board[7][3] = 'R'
                    board[7][0] = ' '

                make_move(board, (from_square, to_square))
                move_history.append((from_square, to_square))
                move_count += 1
                fifty_move_count += 1

                # Check for pawn promotion
                if board[to_square[0]][to_square[1]] == 'P' and to_square[0] == 0:
                    promotion_piece = input("Choose a piece to promote to (Q, R, B, N): ")
                    promote_pawn(board, to_square, promotion_piece)
                else:
                    fifty_move_count = 0

                break
        else:
            # AI's move
            ai_score = make_ai_move(board, depth=2, player='w', alpha=-float('inf'), beta=float('inf'))
            from_square, to_square = move_history.pop()
            print(f"AI's move: {chr(ord('a') + from_square[1])}{from_square[0] + 1} {chr(ord('a') + to_square[1])}{to_square[0] + 1}")
            move_count += 1
            fifty_move_count += 1

        player_turn = not player_turn

if __name__ == "__main__":
    play_game_with_ai()
