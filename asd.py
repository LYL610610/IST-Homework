import tkinter as tk
from tkinter import messagebox
import random
import tkinter.messagebox as messagebox
import time
from typing import List, Tuple


valid_moves = []

# Board Constants
board_size = 8
suquare_size = 60

# GUI Constants
window = tk.Tk()
window.withdraw()
menu = tk.Menu(window)

# Game State Variables
board = [[None] * board_size for _ in range(board_size)]
selected_piece = None
ai_difficulty = "Easy"
game_over = False

# Player Colors
PLAYER_COLOR = "white"
AI_COLOR = "black"
PLAYER_KING_COLOR = "green"
AI_KING_COLOR = "yellow"

# Piece Values
NORMAL_VALUE = 10
KING_VALUE = 20
EDGE_VALUE = 5
CENTER_VALUE = 3

def clear_canvas():
    canvas.delete("all")

def draw_board():
    for row in range(8):
        for col in range(8):
            draw_square(row, col)

def draw_square(row, col):
    x1, y1 = col * 60, row * 60
    x2, y2 = x1 + 60, y1 + 60
    if (row + col) % 2 == 0:
        canvas.create_rectangle(x1, y1, x2, y2, fill="#8B4513")

def draw_pieces():
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece is not None:
                draw_piece(row, col, piece)

def draw_piece(row, col, piece):
    x1, y1 = col * 60, row * 60
    x2, y2 = x1 + 60, y1 + 60
    color = "white" if piece == "white" else "black" if piece == "black" else "blue" if piece == "green" else "red"
    canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill=color)

def mark_selected_and_valid_moves():
    if selected_piece is not None:
        for row, col in get_valid_moves(board, selected_piece[0], selected_piece[1]):
            mark_square(row, col)

def mark_square(row, col):
    x1, y1 = col * 60, row * 60
    x2, y2 = x1 + 60, y1 + 60
    canvas.create_rectangle(x1 + 2, y1 + 2, x2 - 2, y2 - 2, outline="black", width=4)

def update_canvas():
    canvas.update()

def start_board():
    clear_canvas()
    draw_board()
    draw_pieces()
    mark_selected_and_valid_moves()
    update_canvas()



def is_within_board(row, col):
    # 检查给定的行和列是否在棋盘内
    return 0 <= row < 8 and 0 <= col < 8

def is_square_empty(game_board, row, col):
    # 检查给定的棋盘位置是否为空
    return game_board[row][col] is None

def is_normal_move(start_row, end_row):
    # 检查是否为普通移动（即只移动一格）
    return abs(end_row - start_row) == 1

def is_jump_move(start_row, end_row):
    # 检查是否为跳跃移动（即跳过一个棋子）
    return abs(end_row - start_row) == 2

def is_valid_jump(game_board, start_row, start_col, end_row, end_col):
    # 检查跳跃是否合法（即跳过的棋子是否为对手的棋子）
    mid_row, mid_col = (start_row + end_row) // 2, (start_col + end_col) // 2
    return game_board[mid_row][mid_col] not in (None, game_board[start_row][start_col])

# def check_move(game_board, start_row, start_col, end_row, end_col):
#     # 检查从起始位置到目标位置的移动是否合法
#     if not is_within_board(end_row, end_col) or not is_square_empty(game_board, end_row, end_col):
#         return False
#     if is_normal_move(start_row, end_row):
#         return True
#     elif is_jump_move(start_row, end_row):
#         return is_valid_jump(game_board, start_row, start_col, end_row, end_col)
#     return False
def check_move(game_board, start_row, start_col, end_row, end_col):
    # 检查从起始位置到目标位置的移动是否合法
    if not is_within_board(end_row, end_col) or not is_square_empty(game_board, end_row, end_col):
        return False
    if game_board[start_row][start_col] == "black" and start_row >= end_row:
        return False  # 如果是黑棋，只能向下移动
    if game_board[start_row][start_col] == "white" and start_row <= end_row:
        return False  # 如果是白棋，只能向上移动
    if is_normal_move(start_row, end_row):
        return True
    elif is_jump_move(start_row, end_row):
        return is_valid_jump(game_board, start_row, start_col, end_row, end_col)
    return False



# Returns all legal moves for a piece, parameters are the board, row number, and column number
# Function to get all possible legal moves for a given piece
def get_possible_moves(board, row, col):
    # 获取给定棋子可能的移动方向和距离
    piece = board[row][col]
    if piece in ("white", "red"):
        directions = ((-1, -1), (-1, 1))  # 白棋或红棋（即白色的王棋）只能向上移动
    elif piece == "black":
        directions = ((1, -1), (1, 1))  # 黑棋只能向下移动
    else:
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))  # 王棋可以向任何方向移动

    possible_moves = []
    for dx, dy in directions:
        for dist in (1, 2):
            possible_moves.append((row + dx * dist, col + dy * dist))
    return possible_moves


def filter_valid_moves(board, row, col, possible_moves):
    # 过滤出合法的移动
    valid_moves = []
    for new_row, new_col in possible_moves:
        if check_move(board, row, col, new_row, new_col):
            valid_moves.append((new_row, new_col))
    return valid_moves

def get_valid_moves(board, row, col):
    # 获取给定棋子的所有合法移动
    possible_moves = get_possible_moves(board, row, col)
    return filter_valid_moves(board, row, col, possible_moves)


def get_jump_moves(row, col):
    # 获取给定棋子可能的跳跃方向
    jump_moves = []
    for dx, dy in ((-1, -1), (-1, 1), (1, -1), (1, 1)):
        jump_moves.append((row + dx * 2, col + dy * 2))
    return jump_moves

def has_valid_jump(board, row, col, jump_moves):
    # 检查是否有合法的跳跃
    for new_row, new_col in jump_moves:
        if check_move(board, row, col, new_row, new_col):
            return True
    return False

def jump_check(row, col):
    # 检查给定位置的棋子是否有跳跃的可能
    jump_moves = get_jump_moves(row, col)
    return has_valid_jump(board, row, col, jump_moves)


def cross_board_check(x, y):
    # Check if a coordinate is on the board
    return 0 <= x < 8 and 0 <= y < 8

def is_black_piece_at_top(x, y):
    # 检查给定位置是否有黑棋，并且在棋盘的顶部
    return board[x][y] == "black" and x == 0

def is_white_piece_at_bottom(x, y):
    # 检查给定位置是否有白棋，并且在棋盘的底部
    return board[x][y] == "white" and x == 7

def become_king(x, y):
    # 检查给定位置的棋子是否应该成为王棋
    if is_black_piece_at_top(x, y):
        board[x][y] = "green"
    elif is_white_piece_at_bottom(x, y):
        board[x][y] = "red"


def piece_move(board, start_row, start_col, end_row, end_col, is_crowning=False):
    # Get the color of the piece
    piece_color = board[start_row][start_col]

    # Check if it's a jump move
    is_jump_move = abs(end_row - start_row) > 1

    if is_jump_move:
        # Calculate the position of the captured piece
        middle_row = (start_row + end_row) // 2
        middle_col = (start_col + end_col) // 2

        # Remove the captured piece
        board[middle_row][middle_col] = None

    # Move the piece to the target position
    board[end_row][end_col] = piece_color

    # Check if it needs to be crowned
    is_player_piece = piece_color == PLAYER_COLOR
    is_ai_piece = piece_color == AI_COLOR
    reached_opponent_end = (is_player_piece and end_row == 0) or (is_ai_piece and end_row == 8 - 1)

    if reached_opponent_end:
        board[end_row][end_col] = PLAYER_KING_COLOR if is_player_piece else AI_KING_COLOR

    # Clear the starting position
    board[start_row][start_col] = None

    return board


def get_all_moves(board: List[List[str]], color: str) -> List[Tuple[int, int, int, int]]:
    all_moves = [(row, col, *move)
                 for row in range(8)
                 for col in range(8)
                 if board[row][col] in {color, color.upper()}
                 for move in get_valid_moves(board, row, col)]
    # Check if there are any jumps
    jumps = [move for move in all_moves if abs(move[0] - move[2]) > 1]
    if jumps:
        return jumps
    else:
        return all_moves


def evaluate(board: List[List[str]], color: str) -> int:
    color_map = {PLAYER_KING_COLOR: 7, AI_KING_COLOR: -7, PLAYER_COLOR: 1, AI_COLOR: -1}
    return sum(color_map.get(board[row][col], 0) for row in range(8) for col in range(8) if board[row][col])

def deep_copy(obj):
    return [deep_copy(item) for item in obj] if isinstance(obj, list) else obj

def alpha_beta_search(board, depth, alpha, beta, is_ai_turn):
    if check_game_over() or depth == 0:
        return evaluate(board, AI_COLOR), None
    moves = get_all_moves(board, AI_COLOR if is_ai_turn else PLAYER_COLOR)
    if not moves:
        return (-float('inf'), None) if is_ai_turn else (float('inf'), None)
    best_score = -float('inf') if is_ai_turn else float('inf')
    best_move = None
    for move in moves:
        new_board = deep_copy(board)
        piece_move(new_board, *move)
        score, _ = alpha_beta_search(new_board, depth - 1, alpha, beta, not is_ai_turn)
        if is_ai_turn and score > best_score:
            best_score = score
            best_move = move
            alpha = max(alpha, best_score)
        if not is_ai_turn and score < best_score:
            best_score = score
            best_move = move
            beta = min(beta, best_score)
        if beta <= alpha:
            break
    return best_score, best_move if best_move else moves[0]

def ai_piece_move():
    time.sleep(0.5)
    best_move = None
    row, col, is_king = None, None, None

    if ai_difficulty == "Easy":
        moves = [(r, c, move[0], move[1]) for r in range(8) for c in range(8)
                 if board[r][c] in [AI_COLOR, AI_KING_COLOR]
                 for move in get_valid_moves(board, r, c)]
        if moves:
            must_jump = any(abs(move[0] - move[2]) > 1 for move in moves)
            moves = [move for move in moves if abs(move[0] - move[2]) > 1] if must_jump else moves
            random_move = random.choice(moves)
            piece_move(board, *random_move)
            start_board()
            row, col = random_move[2], random_move[3]
            is_king = become_king(row, col)

    else:
        depth = 2 if ai_difficulty == "Medium" else 4
        _, best_move = alpha_beta_search(board, depth, -float('inf'), float('inf'), True)
        if best_move:
            piece_move(board, *best_move)
            start_board()
            row, col = best_move[2], best_move[3]
            is_king = become_king(row, col)

    while best_move and not is_king and jump_check(row, col):
        _, best_move = alpha_beta_search(board, 4, -float('inf'), float('inf'), True)
        if best_move:
            piece_move(board, *best_move)
            start_board()
            row, col = best_move[2], best_move[3]
            is_king = become_king(row, col)

    if check_game_over():
        ending_message()
        return True

    return False

def game_setting(difficulty):
    # setting the difficulty
    global ai_difficulty
    ai_difficulty = difficulty

def click_gui(event):
    global selected_piece, valid_moves, game_over
    x, y = event.x, event.y
    row, col = y // 60, x // 60

    if game_over or not cross_board_check(row, col):
        return

    if selected_piece is None:
        if board[row][col] in (PLAYER_COLOR, PLAYER_KING_COLOR):
            selected_piece = (row, col)
            valid_moves = get_valid_moves(board, row, col)
            if any(abs(move[0] - row) > 1 for move in valid_moves):
                valid_moves = [move for move in valid_moves if abs(move[0] - row) > 1]
    else:
        if (row, col) in valid_moves:
            is_king = piece_move(board, selected_piece[0], selected_piece[1], row, col)
            start_board()
            if not is_king and abs(row - selected_piece[0]) > 1 and jump_check(row, col):
                selected_piece = (row, col)
                valid_moves = [move for move in valid_moves if abs(move[0] - row) > 1]
            else:
                selected_piece = None
                ai_piece_move()
        elif board[row][col] in (PLAYER_COLOR, PLAYER_KING_COLOR):
            selected_piece = (row, col)
            valid_moves = get_valid_moves(board, row, col)
            if any(abs(move[0] - row) > 1 for move in valid_moves):
                valid_moves = [move for move in valid_moves if abs(move[0] - row) > 1]
        else:
            selected_piece = None

    start_board()

def check_game_over():
    player_pieces, ai_pieces = 0, 0
    player_has_valid_moves, ai_has_valid_moves = False, False

    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece in (PLAYER_COLOR, PLAYER_KING_COLOR):
                player_pieces += 1
                if not player_has_valid_moves and get_valid_moves(board, row, col):
                    player_has_valid_moves = True
            elif piece in (AI_COLOR, AI_KING_COLOR):
                ai_pieces += 1
                if not ai_has_valid_moves and get_valid_moves(board, row, col):
                    ai_has_valid_moves = True

    if player_pieces == 0 or ai_pieces == 0:
        return True

    if not player_has_valid_moves and not ai_has_valid_moves:
        return True

    return False

def showing_rules():
    # Display rule descriptions
    messagebox.showinfo("Game Rules",
                        "This is a game of International 64-square Draughts.\n"
                        "The game rules are as follows:\n"
                        "1. Each player occupies one corner with a different color.\n"
                        "2. Pieces can move or jump over other pieces in any of the six adjacent directions connected in a straight line.\n"
                        "3. The first player to occupy all the positions directly opposite wins.\n"
                        "4. If a player's piece captures the opponent's king, it will immediately be crowned king and the game ends.\n"
                        "5. The king is produced when one's piece reaches the last line on the opposite side.\n"
                        "6. The king can move or jump over other pieces in any direction.\n"
                        "Enjoy your game!")

def restart_game():
    global board, game_over
    board = [[None] * 8 for _ in range(8)]
    initialize_board()

    game_over = False

    start_board()

def ending_message():
    player_pieces = 0
    ai_pieces = 0
    player_has_valid_moves = False
    ai_has_valid_moves = False

    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece in (PLAYER_COLOR, PLAYER_KING_COLOR):
                player_pieces += 1
                if not player_has_valid_moves and get_valid_moves(board, row, col):
                    player_has_valid_moves = True
            elif piece in (AI_COLOR, AI_KING_COLOR):
                ai_pieces += 1
                if not ai_has_valid_moves and get_valid_moves(board, row, col):
                    ai_has_valid_moves = True

    if player_pieces == 0 or not player_has_valid_moves:
        message = 'AI won!'
    else:
        message = 'You won!'

    message_window(message)

    game_over = True

def message_window(message):
    top = tk.Toplevel()
    top.title('Game Over')

    label = tk.Label(top, text=message, font=('Arial', 24))
    label.pack(padx=20, pady=20)

    close_button = tk.Button(top, text='Close Window', command=top.destroy)
    close_button.pack(pady=10)

    restart_button = tk.Button(top, text='Restart Game', command=lambda: refreash(top))
    restart_button.pack(pady=10)

def refreash(top):
    top.destroy()
    restart_game()

def initialize_board():
    # Initialize the board state
    for row in range(3):
        for col in range(8):
            if (row + col) % 2 == 1:
                board[row][col] = AI_COLOR
    for row in range(5, 8):
        for col in range(8):
            if (row + col) % 2 == 1:
                board[row][col] = PLAYER_COLOR

def create_menu(window):
    # Create menu
    menu = tk.Menu(window)
    window.config(menu=menu)

    # Add menu items
    rules_menu = tk.Menu(menu)
    menu.add_cascade(label="Game Rules", menu=rules_menu)
    rules_menu.add_command(label="View Rules", command=showing_rules)

    difficulty_menu = tk.Menu(menu)
    menu.add_cascade(label="Difficulty Level", menu=difficulty_menu)
    difficulty_menu.add_command(label="Easy", command=lambda: game_setting("Easy"))
    difficulty_menu.add_command(label="Medium", command=lambda: game_setting("Medium"))
    difficulty_menu.add_command(label="Hard", command=lambda: game_setting("Hard"))
    menu.add_command(label="Restart Game", command=restart_game)


if __name__ == "__main__":
    # Create window and canvas
    window = tk.Tk()
    window.title("Checkers")
    canvas = tk.Canvas(window, width=8 * 60, height=8 * 60)
    canvas.pack()

    # Initialize board and bind event
    initialize_board()
    canvas.bind("<Button-1>", click_gui)

    # Create menu and draw board
    create_menu(window)
    start_board()

    window.mainloop()