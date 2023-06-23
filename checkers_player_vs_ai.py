from tkinter import *
import random
import time
import copy
from tkinter import messagebox

# 创建主窗口
main_window = Tk()  
main_window.title('Checkers')

# 定义开始新游戏的回调函数
def restart_game():
    start_new_game()
    draw(-1, -1, -1, -1)

# 定义选择游戏难度的回调函数-普通
def select_difficulty_normal():
    global alpha,beta
    alpha = float('inf')
    beta = float('-inf')
    return alpha,beta

# 定义选择游戏难度的回调函数-普通
def select_difficulty_hard():
    global alpha, beta
    alpha = float('-inf')
    beta = float('inf')
    return alpha,beta

# 菜单栏
menu_bar = Menu(main_window)
# 创建开始新游戏的菜单
game_menu = Menu(menu_bar, tearoff=0)
game_menu.add_command(label="Start New Game", command=restart_game)
menu_bar.add_cascade(label="Game", menu=game_menu)

# 创建选择游戏难度的菜单
difficulty_menu = Menu(menu_bar, tearoff=0)
difficulty_menu.add_command(label="Normal", command=select_difficulty_normal)
difficulty_menu.add_command(label="Hard", command=select_difficulty_hard)
menu_bar.add_cascade(label="Difficulty", menu=difficulty_menu)

# 将菜单栏添加到主窗口
main_window.config(menu=menu_bar)
desk = Canvas(main_window, width=800, height=800, bg='#FFFFFF')
desk.pack()

# 初始化一些全局变量
possible_moves_list = ()
game_state = 3
player_score = 0
ai_score = 0
selected_piece_x = -1
is_player_move = True
alpha = float('-inf')
beta = float('inf')

# 开始新游戏，初始化棋盘
def start_new_game(): 
    global field
    field = [[0, 3, 0, 3, 0, 3, 0, 3],
             [3, 0, 3, 0, 3, 0, 3, 0],
             [0, 3, 0, 3, 0, 3, 0, 3],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [1, 0, 1, 0, 1, 0, 1, 0],
             [0, 1, 0, 1, 0, 1, 0, 1],
             [1, 0, 1, 0, 1, 0, 1, 0]]

# 绘制棋盘和棋子
# def draw(start_x, start_y, end_x, end_y):
#     global field, red_border, green_border
#     cell_size = 100
#     desk.delete('all')
#     red_border = desk.create_rectangle(-5, -5, -5, -5, outline="red", width=5)
#     green_border = desk.create_rectangle(-5, -5, -5, -5, outline="green", width=5)
#
#     # 绘制棋盘
#     for x in range(0, 8 * cell_size, 2 * cell_size):
#         for y in range(cell_size, 8 * cell_size, 2 * cell_size):
#             desk.create_rectangle(x, y, x + cell_size, y + cell_size, fill="black")
#     for x in range(cell_size, 8 * cell_size, 2 * cell_size):
#         for y in range(0, 8 * cell_size, 2 * cell_size):
#             desk.create_rectangle(x, y, x + cell_size, y + cell_size, fill="black")
#
#     # 绘制棋子
#     for y in range(8):
#         for x in range(8):
#             piece_type = field[y][x]
#             if piece_type:
#                 color = 'black' if piece_type in [1,2] else 'white'
#                 desk.create_oval(x*cell_size+5, y*cell_size+5, (x+1)*cell_size-5, (y+1)*cell_size-5, fill=color, outline='#6E7B8B', width=7)
#                 if piece_type in [2,4]:
#                     desk.create_oval(x*cell_size+5, y*cell_size+5, (x+1)*cell_size-5, (y+1)*cell_size-5, fill=color, outline='red', width=7)
#
#     # 绘制移动的棋子
#     piece_type = field[start_y][start_x]
#     if piece_type:
#         color = 'black' if piece_type in [1, 2] else 'white'
#         desk.create_oval(start_x*cell_size+5, start_y*cell_size+5, (start_x+1)*cell_size-5, (start_y+1)*cell_size-5, fill=color, outline='#6E7B8B', width=7 ,tag='ani')

def draw(start_x, start_y, end_x, end_y):
    global field, red_border, green_border
    cell_size = 100
    desk.delete('all')
    red_border = desk.create_rectangle(-5, -5, -5, -5, outline="red", width=5)
    green_border = desk.create_rectangle(-5, -5, -5, -5, outline="green", width=5)

    # 绘制棋盘
    for x in range(0, 8 * cell_size, 2 * cell_size):
        for y in range(cell_size, 8 * cell_size, 2 * cell_size):
            desk.create_rectangle(x, y, x + cell_size, y + cell_size, fill="white")  # 红色方块
    for x in range(cell_size, 8 * cell_size, 2 * cell_size):
        for y in range(0, 8 * cell_size, 2 * cell_size):
            desk.create_rectangle(x, y, x + cell_size, y + cell_size, fill="white")  # 黑色方块

    # 对于剩下的白色方块，我们也需要将它们填充为黑色
    for x in range(0, 8 * cell_size, 2 * cell_size):
        for y in range(0, 8 * cell_size, 2 * cell_size):
            desk.create_rectangle(x, y, x + cell_size, y + cell_size, fill="darkred")  # 黑色方块
    for x in range(cell_size, 8 * cell_size, 2 * cell_size):
        for y in range(cell_size, 8 * cell_size, 2 * cell_size):
            desk.create_rectangle(x, y, x + cell_size, y + cell_size, fill="darkred")  # 黑色方块

    # 绘制棋子
    for y in range(8):
        for x in range(8):
            piece_type = field[y][x]
            if piece_type:
                color = 'white' if piece_type in [1, 2] else 'black'  # 改变棋子的颜色
                desk.create_oval(x * cell_size + 5, y * cell_size + 5, (x + 1) * cell_size - 5,
                                 (y + 1) * cell_size - 5, fill=color, outline='grey', width=4)
                if piece_type in [2, 4]:
                    desk.create_oval(x * cell_size + 5, y * cell_size + 5, (x + 1) * cell_size - 5,
                                     (y + 1) * cell_size - 5, fill=color, outline='gold', width=4)  # 改变王棋的颜色

    # 绘制移动的棋子
    piece_type = field[start_y][start_x]
    if piece_type:
        color = 'white' if piece_type in [1, 2] else 'black'
        desk.create_oval(start_x * cell_size + 5, start_y * cell_size + 5, (start_x + 1) * cell_size - 5,
                         (start_y + 1) * cell_size - 5, fill=color, outline='grey', width=4, tag='ani')

    # 绘制移动动画
    move_x = 1 if start_x < end_x else -1
    move_y = 1 if start_y < end_y else -1
    for i in range(abs(start_x - end_x)):
        for j in range(33):
            speed = (33 - j) / 33  # 速度在移动过程中逐渐减小
            desk.move('ani', 3 * move_x * speed, 3 * move_y * speed)
            desk.update()
            time.sleep(0.01)


# 显示游戏结束的消息，并询问玩家是否要开始新游戏
def show_end_message(end_reason):
    global is_player_move, i
    end_message = 'Game Over'
    if end_reason == 1:
        i = messagebox.askyesno(title=end_message, message='You won!\nClick "Yes" to start a new game.', icon='info')
    if end_reason == 2:
        i = messagebox.askyesno(title=end_message, message='You lost!\nClick "Yes" to start a new game.', icon='info')
    if end_reason == 3:
        m = messagebox.askyesno(title=end_message, message='No more moves.\nClick "Yes" to start a new game.', icon='info')
    if i:
        start_new_game()
        draw(-1, -1, -1, -1)
        is_player_move = True


# 玩家点击棋盘时的处理函数
# def position_1(event):
#     x, y = event.x // 100, event.y // 100
#     desk.coords(green_border, x * 100, y * 100, x * 100 + 100, y * 100 + 100)

# 玩家释放鼠标按钮时的处理函数
# def position_2(event):
#     global selected_piece_x, selected_piece_y, target_x, target_y
#     global is_player_move
#     x, y = event.x // 100, event.y // 100
#     if field[y][x] == 1 or field[y][x] == 2:
#         desk.coords(red_border, x * 100, y * 100, x * 100 + 100, y * 100 + 100)
#         selected_piece_x, selected_piece_y = x, y
#         # 检查是否有可以跳吃的棋子
#         has_jump_moves = has_jump_moves_available()
#         if has_jump_moves:
#             print(can_piece_jump(selected_piece_x, selected_piece_y))
#             if not can_piece_jump(selected_piece_x, selected_piece_y):
#                 messagebox.showinfo("提示", "当前有可以跳吃的棋子，请选择可以跳吃的棋子！")
#     else:
#         if selected_piece_x != -1:  # клетка выбрана
#             target_x, target_y = x, y
#             if is_player_move:  # ход игрока?
#                 player_turn()
#                 if not is_player_move:
#                     time.sleep(0.5)
#                     computer_turn()
#             selected_piece_x = -1
#             desk.coords(red_border, -5, -5, -5, -5)

# 处理玩家点击棋盘时的事件
def handle_board_click(event):
    grid_x, grid_y = event.x // 100, event.y // 100
    desk.coords(green_border, grid_x * 100, grid_y * 100, grid_x * 100 + 100, grid_y * 100 + 100)

# 处理玩家释放鼠标按钮时的事件
def handle_mouse_release(event):
    global selected_piece_x, selected_piece_y, target_x, target_y
    global is_player_move
    grid_x, grid_y = event.x // 100, event.y // 100
    if field[grid_y][grid_x] == 1 or field[grid_y][grid_x] == 2:
        desk.coords(red_border, grid_x * 100, grid_y * 100, grid_x * 100 + 100, grid_y * 100 + 100)
        selected_piece_x, selected_piece_y = grid_x, grid_y
        # 检查是否有可以跳吃的棋子
        has_jump_moves = has_jump_moves_available()
        if has_jump_moves:
            print(can_piece_jump(selected_piece_x, selected_piece_y))
            if not can_piece_jump(selected_piece_x, selected_piece_y):
                messagebox.showinfo("提示", "当前有可以跳吃的棋子，请选择可以跳吃的棋子！")
    else:
        if selected_piece_x != -1:  # 如果已经选择了棋子
            target_x, target_y = grid_x, grid_y
            if is_player_move:  # 如果是玩家的回合
                player_turn()
                if not is_player_move:
                    time.sleep(0.5)
                    computer_turn()
            selected_piece_x = -1
            desk.coords(red_border, -5, -5, -5, -5)


# # 检查是否有可以跳吃的棋子
# def has_jump_moves_available():
#     if len(check_moves_i1(list_hi())) > 0:
#         return True
#     return False
#
# # 检查指定的棋子是否可以跳吃
# def can_piece_jump(x, y):
#     piece = field[y][x]
#     if piece == 1 or piece == 2:
#         jumps = check_moves_i1p([], x, y)
#         if jumps:
#             return True
#     return False

# Check if there are any pieces that can make a jump move
def has_jump_moves_available():
    return len(check_moves_eat2(get_human_possible_moves())) > 0

# Check if a specific piece can make a jump move
def can_piece_jump(piece_x, piece_y):
    piece = field[piece_y][piece_x]
    if piece in [1, 2]:
        jumps = check_moves_i1p([], piece_x, piece_y)
        return bool(jumps)
    return False


# # 电脑玩家的回合
# def computer_turn():
#     global is_player_move
#     global n2_list
#     check_hk(1, (), [], alpha, beta)
#     if n2_list:
#         kh = len(n2_list)
#         th = random.randint(0, kh - 1)
#         dh = len(n2_list[th])
#         for k in range(dh - 1):
#             my_list = move(1, n2_list[th][k][0], n2_list[th][k][1], n2_list[th][1 + k][0], n2_list[th][1 + k][1])
#         n2_list = []
#         is_player_move = True
#
#     s_k, s_i = scan()
#     if not s_i:
#         show_end_message(2)
#     elif not s_k:
#         show_end_message(1)
#     elif is_player_move and not (list_hi()):
#         show_end_message(3)
#     elif not is_player_move and not (list_hk()):
#         show_end_message(3)

def computer_turn():
    global is_player_move
    global possible_moves_list
    evaluate_all_moves(1, (), [], alpha, beta)
    if possible_moves_list:
        num_possible_moves = len(possible_moves_list)
        chosen_move_index = random.randint(0, num_possible_moves - 1)
        num_steps_in_chosen_move = len(possible_moves_list[chosen_move_index])
        for step in range(num_steps_in_chosen_move - 1):
            move_list = move(1, possible_moves_list[chosen_move_index][step][0], possible_moves_list[chosen_move_index][step][1], possible_moves_list[chosen_move_index][step + 1][0], possible_moves_list[chosen_move_index][step + 1][1])
        possible_moves_list = []
        is_player_move = True
    computer_score, player_score = scan_board()
    if not player_score:
        show_end_message(2)
    elif not computer_score:
        show_end_message(1)
    elif is_player_move and not (get_human_possible_moves()):
        show_end_message(3)
    elif not is_player_move and not (get_computer_possible_moves()):
        show_end_message(3)

# get_computer_possible_moves函数用于获取电脑玩家的所有可能的移动
def get_computer_possible_moves():
    # 首先尝试获取所有可以吃掉对手棋子的移动
    my_list = check_moves_ai([])
    # 如果没有可以吃掉对手棋子的移动，那么获取所有普通的移动
    if not my_list:
        my_list = check_moves_noeat([])
    return my_list

# # evaluate_all_moves函数用于评估电脑玩家的所有可能的移动
# def evaluate_all_moves(tur, n_list, my_list, alpha, beta):
#     global field
#     global possible_moves_list
#     global l_rez, player_score, ai_score
#     if not my_list:
#         my_list = get_computer_possible_moves()
#
#     if my_list:
#         k_pole = copy.deepcopy(field)
#         for ((selected_piece_x, selected_piece_y), (target_x, target_y)) in my_list:
#             t_list = move(0, selected_piece_x, selected_piece_y, target_x, target_y)
#             if t_list:
#                 evaluate_all_moves(tur, (n_list + ((selected_piece_x, selected_piece_y),)), t_list, alpha, beta)
#             else:
#                 check_hi(tur, [], alpha, beta)
#                 if tur == 1:
#                     t_rez = ai_score / player_score
#                     if not possible_moves_list:
#                         possible_moves_list = (n_list + ((selected_piece_x, selected_piece_y), (target_x, target_y)),)
#                         l_rez = t_rez
#                         alpha = max(alpha, t_rez)
#                     else:
#                         if t_rez == l_rez:
#                             possible_moves_list = possible_moves_list + (n_list + ((selected_piece_x, selected_piece_y), (target_x, target_y)),)
#                         if t_rez > l_rez:
#                             possible_moves_list = ()
#                             possible_moves_list = (n_list + ((selected_piece_x, selected_piece_y), (target_x, target_y)),)
#                             l_rez = t_rez
#                             alpha = max(alpha, t_rez)
#                     ai_score = 0
#                     player_score = 0
#
#             field = copy.deepcopy(k_pole)
#             if beta <= alpha:
#                 break
#     else:
#         computer_score, player_score = scan_board()
#         ai_score += (computer_score - player_score)
#         player_score += 1

def evaluate_all_moves(turn, move_sequence, possible_moves, alpha, beta):
    global field
    global possible_moves_list
    global best_score, player_score, ai_score

    # 如果没有给出可能的移动，那么获取电脑的所有可能的移动
    if not possible_moves:
        possible_moves = get_computer_possible_moves()

    # 如果有可能的移动
    if possible_moves:
        # 保存当前的棋盘状态
        original_field = copy.deepcopy(field)

        # 遍历所有可能的移动
        for ((selected_piece_x, selected_piece_y), (target_x, target_y)) in possible_moves:
            # 执行移动
            next_moves = move(0, selected_piece_x, selected_piece_y, target_x, target_y)

            # 如果还有可能的移动
            if next_moves:
                # 递归调用这个函数
                evaluate_all_moves(turn, (move_sequence + ((selected_piece_x, selected_piece_y),)), next_moves, alpha, beta)
            else:
                # 检查人类玩家的所有可能的移动
                check_human_moves(turn, [], alpha, beta)
                # 如果是电脑的回合
                if turn == 1:
                    # 计算得分比例
                    score_ratio = ai_score / player_score

                    # 如果没有可能的移动
                    if not possible_moves_list:
                        # 保存当前的移动序列和得分比例
                        possible_moves_list = (move_sequence + ((selected_piece_x, selected_piece_y), (target_x, target_y)),)
                        best_score = score_ratio
                        alpha = max(alpha, score_ratio)
                    else:
                        # 如果得分比例等于最佳得分
                        if score_ratio == best_score:
                            # 添加当前的移动序列到可能的移动列表
                            possible_moves_list = possible_moves_list + (move_sequence + ((selected_piece_x, selected_piece_y), (target_x, target_y)),)
                        # 如果得分比例大于最佳得分
                        if score_ratio > best_score:
                            # 清空可能的移动列表
                            possible_moves_list = ()
                            # 保存当前的移动序列和得分比例
                            possible_moves_list = (move_sequence + ((selected_piece_x, selected_piece_y), (target_x, target_y)),)
                            best_score = score_ratio
                            alpha = max(alpha, score_ratio)

                    # 重置电脑和玩家的得分
                    ai_score = 0
                    player_score = 0

            # 恢复原始的棋盘状态
            field = copy.deepcopy(original_field)

            # 如果beta小于或等于alpha，那么停止搜索
            if beta <= alpha:
                break
    else:
        # 计算电脑和玩家的得分
        computer_score, player_score = scan_board()
        # 更新电脑的得分
        ai_score += (computer_score - player_score)
        # 更新玩家的得分
        player_score += 1



# # get_human_possible_moves函数用于获取人类玩家的所有可能的移动
# def get_human_possible_moves():
#     # 首先尝试获取所有可以吃掉对手棋子的移动
#     my_list = check_moves_i1([])
#     # 如果没有可以吃掉对手棋子的移动，那么获取所有普通的移动
#     if not my_list:
#         my_list = check_moves_i2([])  # здесь проверяем оставшиеся ходы
#     return my_list
#
# # check_human_moves函数用于评估人类玩家的所有可能的移动
# def check_human_moves(tur, my_list, alpha, beta):
#     global field, player_score, ai_score
#     global game_state
#     if not my_list:
#         my_list = get_human_possible_moves()
#
#     if my_list:
#         k_pole = copy.deepcopy(field)
#         for ((selected_piece_x, selected_piece_y), (target_x, target_y)) in my_list:
#             t_list = move(0, selected_piece_x, selected_piece_y, target_x, target_y)
#             if t_list:
#                 check_human_moves(tur, t_list, alpha, beta)
#             else:
#                 if tur < game_state:
#                     evaluate_all_moves(tur + 1, (), [], alpha, beta)
#                 else:
#                     computer_score, player_score = scan_board()
#                     ai_score += (computer_score - player_score)
#                     player_score += 1
#                     beta = min(beta, ai_score / player_score)
#
#             field = copy.deepcopy(k_pole)
#             if beta <= alpha:
#                 break
#     else:
#         computer_score, player_score = scan_board()
#         ai_score += (computer_score - player_score)
#         player_score += 1
#         beta = min(beta, ai_score / player_score)

# 获取人类玩家所有可能的移动
def get_human_possible_moves():
    # 尝试获取所有可以吃掉对手棋子的移动
    possible_moves = check_moves_eat2([])
    # 如果没有可以吃掉对手棋子的移动，那么获取所有普通的移动
    if not possible_moves:
        possible_moves = check_moves_i2([])
    return possible_moves

# 评估人类玩家所有可能的移动
def check_human_moves(turn, possible_moves, alpha, beta):
    global field, player_score, ai_score
    global game_state
    if not possible_moves:
        possible_moves = get_human_possible_moves()
    if possible_moves:
        original_field = copy.deepcopy(field)
        for ((selected_piece_x, selected_piece_y), (target_x, target_y)) in possible_moves:
            next_moves = move(0, selected_piece_x, selected_piece_y, target_x, target_y)
            if next_moves:
                check_human_moves(turn, next_moves, alpha, beta)
            else:
                if turn < game_state:
                    evaluate_all_moves(turn + 1, (), [], alpha, beta)
                else:
                    computer_score, player_score = scan_board()
                    ai_score += (computer_score - player_score)
                    player_score += 1
                    beta = min(beta, ai_score / player_score)
            field = copy.deepcopy(original_field)
            if beta <= alpha:
                break
    else:
        computer_score, player_score = scan_board()
        ai_score += (computer_score - player_score)
        player_score += 1
        beta = min(beta, ai_score / player_score)

# scan_board函数用于扫描棋盘，统计双方的棋子数量
def scan_board():
    global field
    # 人类玩家的棋子数量
    player_score = 0
    # 电脑玩家的棋子数量
    computer_score = 0
    # 遍历棋盘
    for k in range(8):
        for ii in field[k]:
            # 根据棋子的类型，更新双方的棋子数量
            if ii == 1:
                player_score += 1
            if ii == 2:
                player_score += 3
            if ii == 3:
                computer_score += 1
            if ii == 4:
                computer_score += 3
    return computer_score, player_score

# player_turn函数用于处理人类玩家的回合
def player_turn():
    global selected_piece_x, selected_piece_y, target_x, target_y
    global is_player_move
    is_player_move = False
    # 获取人类玩家的所有可能的移动
    my_list = get_human_possible_moves()
    if my_list:
        # 如果人类玩家选择的移动在所有可能的移动中，那么执行这个移动
        if ((selected_piece_x, selected_piece_y), (target_x, target_y)) in my_list:
            t_list = move(1, selected_piece_x, selected_piece_y, target_x, target_y)
            if t_list:
                is_player_move = True
        else:
            is_player_move = True
    # 更新棋盘
    desk.update()

# move函数用于执行一次移动
# def move(f, selected_piece_x, selected_piece_y, target_x, target_y):
#     global field
#     # 如果是人类玩家的回合，那么在界面上画出这次移动
#     if f: draw(selected_piece_x, selected_piece_y, target_x, target_y)
#     # 如果人类玩家的棋子到达了对方的基地，那么升级这个棋子
#     if target_y == 0 and field[selected_piece_y][selected_piece_x] == 1:
#         field[selected_piece_y][selected_piece_x] = 2
#     # 如果电脑玩家的棋子到达了对方的基地，那么升级这个棋子
#     if target_y == 7 and field[selected_piece_y][selected_piece_x] == 3:
#         field[selected_piece_y][selected_piece_x] = 4
#     # 更新棋盘
#     field[target_y][target_x] = field[selected_piece_y][selected_piece_x]
#     field[selected_piece_y][selected_piece_x] = 0
#
#     # 计算移动的方向
#     kx = ky = 1
#     if selected_piece_x < target_x:
#         kx = -1
#     if selected_piece_y < target_y:
#         ky = -1
#     x_poz, y_poz = target_x, target_y
#     # 如果在移动的过程中吃掉了对方的棋子，那么更新棋盘，并检查是否可以继续吃掉对方的棋子
#     while (selected_piece_x != x_poz) or (selected_piece_y != y_poz):
#         x_poz += kx
#         y_poz += ky
#         if field[y_poz][x_poz] != 0:
#             field[y_poz][x_poz] = 0
#             if f:
#                 draw(-1, -1, -1, -1)
#             if field[target_y][target_x] == 3 or field[target_y][target_x] == 4:
#                 return check_moves_k1p([], target_x, target_y)
#             elif field[target_y][target_x] == 1 or field[target_y][target_x] == 2:
#                 return check_moves_i1p([], target_x, target_y)
#     if f:
#         draw(selected_piece_x, selected_piece_y, target_x, target_y)

def move(is_human_turn, selected_piece_x, selected_piece_y, target_x, target_y):
    global field
    # 如果是人类玩家的回合，那么在界面上画出这次移动
    if is_human_turn:
        draw_move(selected_piece_x, selected_piece_y, target_x, target_y)
    # 检查并升级棋子
    upgrade_piece(selected_piece_x, selected_piece_y, target_x, target_y)
    # 更新棋盘
    update_board(selected_piece_x, selected_piece_y, target_x, target_y)
    # 计算移动的方向
    direction_x, direction_y = calculate_direction(selected_piece_x, selected_piece_y, target_x, target_y)
    # 如果在移动的过程中吃掉了对方的棋子，那么更新棋盘，并检查是否可以继续吃掉对方的棋子
    return check_and_execute_capture(is_human_turn, selected_piece_x, selected_piece_y, target_x, target_y, direction_x, direction_y)

def draw_move(selected_piece_x, selected_piece_y, target_x, target_y):
    draw(selected_piece_x, selected_piece_y, target_x, target_y)

def upgrade_piece(selected_piece_x, selected_piece_y, target_x, target_y):
    if target_y == 0 and field[selected_piece_y][selected_piece_x] == 1:
        field[selected_piece_y][selected_piece_x] = 2
    if target_y == 7 and field[selected_piece_y][selected_piece_x] == 3:
        field[selected_piece_y][selected_piece_x] = 4

def update_board(selected_piece_x, selected_piece_y, target_x, target_y):
    field[target_y][target_x] = field[selected_piece_y][selected_piece_x]
    field[selected_piece_y][selected_piece_x] = 0

def calculate_direction(selected_piece_x, selected_piece_y, target_x, target_y):
    direction_x = -1 if selected_piece_x < target_x else 1
    direction_y = -1 if selected_piece_y < target_y else 1
    return direction_x, direction_y

def check_and_execute_capture(is_human_turn, selected_piece_x, selected_piece_y, target_x, target_y, direction_x, direction_y):
    x_position, y_position = target_x, target_y
    while (selected_piece_x != x_position) or (selected_piece_y != y_position):
        x_position += direction_x
        y_position += direction_y
        if field[y_position][x_position] != 0:
            field[y_position][x_position] = 0
            if is_human_turn:
                draw(-1, -1, -1, -1)
            if field[target_y][target_x] in [3, 4]:
                return check_moves_eat([], target_x, target_y)
            elif field[target_y][target_x] in [1, 2]:
                return check_moves_i1p([], target_x, target_y)
    if is_human_turn:
        draw(selected_piece_x, selected_piece_y, target_x, target_y)


# # check_moves_ai函数用于检查电脑玩家的所有棋子的所有可能的吃子移动
# def check_moves_ai(my_list):
#     for y in range(8):
#         for x in range(8):
#             # 检查每个棋子的所有可能的吃子移动
#             my_list = check_moves_k1p(my_list, x, y)
#     return my_list

# check_moves_ai函数用于检查电脑玩家的所有棋子的所有可能的吃子移动
def check_moves_ai(possible_moves):
    for y_coordinate in range(8):
        for x_coordinate in range(8):
            # 检查每个棋子的所有可能的吃子移动
            possible_moves = check_possible_moves_for_piece(possible_moves, x_coordinate, y_coordinate)
    return possible_moves

def check_possible_moves_for_piece(possible_moves, piece_x, piece_y):
    return check_moves_eat(possible_moves, piece_x, piece_y)


# # check_moves_eat函数用于检查一个棋子的所有可能的吃子移动
# def check_moves_k1p(my_list, x, y):
#     # 如果这个棋子是电脑玩家的普通棋子
#     if field[y][x] == 3:
#         # 检查所有可能的吃子方向
#         for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
#             # 如果吃子的方向是合法的，并且可以吃掉人类玩家的棋子
#             if 0 <= y + iy + iy <= 7 and 0 <= x + ix + ix <= 7:
#                 if field[y + iy][x + ix] == 1 or field[y + iy][x + ix] == 2:
#                     if field[y + iy + iy][x + ix + ix] == 0:
#                         # 添加这个吃子移动到列表中
#                         my_list.append(((x, y), (x + ix + ix, y + iy + iy)))
#     # 如果这个棋子是电脑玩家的王棋
#     if field[y][x] == 4:
#         for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
#             osh = 0
#             for k in range(1, 8):
#                 if 0 <= y + iy * k <= 7 and 0 <= x + ix * k <= 7:
#                     if osh == 1:
#                         # 添加这个吃子移动到列表中
#                         my_list.append(((x, y), (x + ix * k, y + iy * k)))
#                     if field[y + iy * k][x + ix * k] == 1 or field[y + iy * k][x + ix * k] == 2:
#                         osh += 1
#                     if field[y + iy * k][x + ix * k] == 3 or field[y + iy * k][x + ix * k] == 4 or osh == 2:
#                         if osh > 0:
#                             # 如果不能吃子，那么删除这个移动
#                             my_list.pop()
#                         break
#     return my_list

# check_moves_eat函数用于检查一个棋子的所有可能的吃子移动
def check_moves_eat(possible_moves, piece_x, piece_y):
    # 如果这个棋子是电脑玩家的普通棋子
    if field[piece_y][piece_x] == 3:
        # 检查所有可能的吃子方向
        possible_moves = check_regular_piece_moves(possible_moves, piece_x, piece_y)
    # 如果这个棋子是电脑玩家的王棋
    elif field[piece_y][piece_x] == 4:
        possible_moves = check_king_piece_moves(possible_moves, piece_x, piece_y)
    return possible_moves

def check_regular_piece_moves(possible_moves, piece_x, piece_y):
    for direction_x, direction_y in (-1, -1), (-1, 1), (1, -1), (1, 1):
        # 如果吃子的方向是合法的，并且可以吃掉人类玩家的棋子
        if is_valid_direction(piece_x, piece_y, direction_x * 2, direction_y * 2):
            if is_opponent_piece(piece_x, piece_y, direction_x, direction_y):
                if is_empty_spot(piece_x, piece_y, direction_x * 2, direction_y * 2):
                    # 添加这个吃子移动到列表中
                    possible_moves.append(((piece_x, piece_y), (piece_x + direction_x * 2, piece_y + direction_y * 2)))
    return possible_moves

def check_king_piece_moves(possible_moves, piece_x, piece_y):
    for direction_x, direction_y in (-1, -1), (-1, 1), (1, -1), (1, 1):
        opponent_encountered = 0
        for step in range(1, 8):
            if is_valid_direction(piece_x, piece_y, direction_x * step, direction_y * step):
                if opponent_encountered == 1:
                    # 添加这个吃子移动到列表中
                    possible_moves.append(((piece_x, piece_y), (piece_x + direction_x * step, piece_y + direction_y * step)))
                if is_opponent_piece(piece_x, piece_y, direction_x * step, direction_y * step):
                    opponent_encountered += 1
                if is_own_piece(piece_x, piece_y, direction_x * step, direction_y * step) or opponent_encountered == 2:
                    if opponent_encountered > 0:
                        # 如果不能吃子，那么删除这个移动
                        possible_moves.pop()
                    break
    return possible_moves

def is_valid_direction(piece_x, piece_y, direction_x, direction_y):
    return 0 <= piece_y + direction_y <= 7 and 0 <= piece_x + direction_x <= 7

def is_opponent_piece(piece_x, piece_y, direction_x, direction_y):
    return field[piece_y + direction_y][piece_x + direction_x] in [1, 2]

def is_own_piece(piece_x, piece_y, direction_x, direction_y):
    return field[piece_y + direction_y][piece_x + direction_x] in[3, 4]

def is_empty_spot(piece_x, piece_y, direction_x, direction_y):
    return field[piece_y + direction_y][piece_x + direction_x] == 0


# # check_moves_k2p函数用于检查电脑玩家的所有棋子的所有可能的非吃子移动
# def check_moves_k2p(my_list):
#     for y in range(8):
#         for x in range(8):
#             # 如果这个棋子是电脑玩家的普通棋子
#             if field[y][x] == 3:
#                 # 检查所有可能的非吃子方向
#                 for ix, iy in (-1, 1), (1, 1):
#                     if 0 <= y + iy <= 7 and 0 <= x + ix <= 7:
#                         # 如果这个方向是空的，那么可以移动
#                         if field[y + iy][x + ix] == 0:
#                             my_list.append(((x, y), (x + ix, y + iy)))
#                         # 如果这个方向是人类玩家的棋子，那么可以吃子
#                         if field[y + iy][x + ix] == 1 or field[y + iy][x + ix] == 2:
#                             if 0 <= y + iy * 2 <= 7 and 0 <= x + ix * 2 <= 7:
#                                 if field[y + iy * 2][x + ix * 2] == 0:
#                                     my_list.append(((x, y), (
#                                         x + ix * 2, y + iy * 2)))
#             # 如果这个棋子是电脑玩家的王棋
#             if field[y][x] == 4:
#                 # 检查所有可能的非吃子方向
#                 for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
#                     osh = 0
#                     for k in range(1, 8):
#                         if 0 <= y + iy * k <= 7 and 0 <= x + ix * k <= 7:
#                             # 如果这个方向是空的，那么可以移动
#                             if field[y + iy * k][x + ix * k] == 0:
#                                 my_list.append(((x, y), (x + ix * k, y + iy * k)))
#                             # 如果这个方向是人类玩家的棋子，那么可以吃子
#                             if field[y + iy * k][x + ix * k] == 1 or field[y + iy * k][x + ix * k] == 2:
#                                 osh += 1
#                             # 如果这个方向是电脑玩家的棋子，那么不能移动
#                             if field[y + iy * k][x + ix * k] == 3 or field[y + iy * k][x + ix * k] == 4 or osh == 2:
#                                 break
#     return my_list

# check_moves_noeat函数用于检查电脑玩家的所有棋子的所有可能的非吃子移动
def check_moves_noeat(possible_moves):
    for y_coordinate in range(8):
        for x_coordinate in range(8):
            # 如果这个棋子是电脑玩家的普通棋子
            if field[y_coordinate][x_coordinate] == 3:
                # 检查所有可能的非吃子方向
                possible_moves = check_regular_piece_non_capture_moves(possible_moves, x_coordinate, y_coordinate)
            # 如果这个棋子是电脑玩家的王棋
            elif field[y_coordinate][x_coordinate] == 4:
                # 检查所有可能的非吃子方向
                possible_moves = check_king_piece_non_capture_moves(possible_moves, x_coordinate, y_coordinate)
    return possible_moves

def check_regular_piece_non_capture_moves(possible_moves, piece_x, piece_y):
    for direction_x, direction_y in (-1, 1), (1, 1):
        if is_valid_direction(piece_x, piece_y, direction_x, direction_y):
            # 如果这个方向是空的，那么可以移动
            if is_empty_spot(piece_x, piece_y, direction_x, direction_y):
                possible_moves.append(((piece_x, piece_y), (piece_x + direction_x, piece_y + direction_y)))
            # 如果这个方向是人类玩家的棋子，那么可以吃子
            if is_opponent_piece(piece_x, piece_y, direction_x, direction_y):
                if is_valid_direction(piece_x, piece_y, direction_x * 2, direction_y * 2) and is_empty_spot(piece_x, piece_y, direction_x * 2, direction_y * 2):
                    possible_moves.append(((piece_x, piece_y), (piece_x + direction_x * 2, piece_y + direction_y * 2)))
    return possible_moves

def check_king_piece_non_capture_moves(possible_moves, piece_x, piece_y):
    for direction_x, direction_y in (-1, -1), (-1, 1), (1, -1), (1, 1):
        opponent_encountered = 0
        for step in range(1, 8):
            if is_valid_direction(piece_x, piece_y, direction_x * step, direction_y * step):
                # 如果这个方向是空的，那么可以移动
                if is_empty_spot(piece_x, piece_y, direction_x * step, direction_y * step):
                    possible_moves.append(((piece_x, piece_y), (piece_x + direction_x * step, piece_y + direction_y * step)))
                # 如果这个方向是人类玩家的棋子，那么可以吃子
                if is_opponent_piece(piece_x, piece_y, direction_x * step, direction_y * step):
                    opponent_encountered += 1
                # 如果这个方向是电脑玩家的棋子，那么不能移动
                if is_own_piece(piece_x, piece_y, direction_x * step, direction_y * step) or opponent_encountered == 2:
                    break
    return possible_moves



# # check_moves_i1函数用于检查人类玩家的所有棋子的所有可能的吃子移动
# def check_moves_i1(my_list):
#     my_list = []
#     for y in range(8):
#         for x in range(8):
#             # 检查每个棋子的所有可能的吃子移动
#             my_list = check_moves_i1p(my_list, x, y)
#     return my_list

# check_moves_eat2函数用于检查人类玩家的所有棋子的所有可能的吃子移动
def check_moves_eat2(possible_moves):
    possible_moves = []
    for y in range(8):
        for x in range(8):
            possible_moves = check_moves_i1p(possible_moves, x, y)
    return possible_moves



# check_moves_i1p函数用于检查一个棋子的所有可能的吃子移动
def check_moves_i1p(my_list, x, y):
    # 如果这个棋子是人类玩家的普通棋子
    if field[y][x] == 1:
        # 检查所有可能的吃子方向
        for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
            if 0 <= y + iy + iy <= 7 and 0 <= x + ix + ix <= 7:
                # 如果吃子的方向是合法的，并且可以吃掉电脑玩家的棋子
                if field[y + iy][x + ix] == 3 or field[y + iy][x + ix] == 4:
                    if field[y + iy + iy][x + ix + ix] == 0:
                        # 添加这个吃子移动到列表中
                        my_list.append(((x, y), (x + ix + ix, y + iy + iy)))
    # 检查所有可能的吃子方向
    if field[y][x] == 2:  # пешка с короной
        for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
            osh = 0  # определение правильности хода
            for k in range(1, 8):
                if 0 <= y + iy * k <= 7 and 0 <= x + ix * k <= 7:
                    if osh == 1:
                        # 添加这个吃子移动到列表中
                        my_list.append(((x, y), (x + ix * k, y + iy * k)))
                    # 如果这个方向是电脑玩家的棋子，那么可以吃子
                    if field[y + iy * k][x + ix * k] == 3 or field[y + iy * k][x + ix * k] == 4:
                        osh += 1
                    # 如果这个方向是人类玩家的棋子，那么不能移动
                    if field[y + iy * k][x + ix * k] == 1 or field[y + iy * k][x + ix * k] == 2 or osh == 2:
                        if osh > 0:
                            # 如果不能吃子，那么删除这个移动
                            my_list.pop()
                        break
    return my_list

# check_moves_i2函数用于检查人类玩家的所有棋子的所有可能的非吃子移动
def check_moves_i2(my_list):
    for y in range(8):  # сканируем всё поле
        for x in range(8):
            # 如果这个棋子是人类玩家的普通棋子
            if field[y][x] == 1:
                # 检查所有可能的非吃子方向
                for ix, iy in (-1, -1), (1, -1):
                    if 0 <= y + iy <= 7 and 0 <= x + ix <= 7:
                        # 如果这个方向是空的，那么可以移动
                        if field[y + iy][x + ix] == 0:
                            my_list.append(((x, y), (x + ix, y + iy)))
                        # 如果这个方向是电脑玩家的棋子，那么可以吃子
                        if field[y + iy][x + ix] == 3 or field[y + iy][x + ix] == 4:
                            if 0 <= y + iy * 2 <= 7 and 0 <= x + ix * 2 <= 7:
                                if field[y + iy * 2][x + ix * 2] == 0:
                                    my_list.append(((x, y), (
                                        x + ix * 2, y + iy * 2)))
            if field[y][x] == 2:
                # 检查所有可能的非吃子方向
                for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
                    osh = 0
                    for k in range(1, 8):
                        if 0 <= y + iy * k <= 7 and 0 <= x + ix * k <= 7:
                            # 如果这个方向是空的，那么可以移动
                            if field[y + iy * k][x + ix * k] == 0:
                                my_list.append(((x, y), (x + ix * k, y + iy * k)))
                            # 如果这个方向是电脑玩家的棋子，那么可以吃子
                            if field[y + iy * k][x + ix * k] == 3 or field[y + iy * k][x + ix * k] == 4:
                                osh += 1
                            # 如果这个方向是人类玩家的棋子，那么不能移动
                            if field[y + iy * k][x + ix * k] == 1 or field[y + iy * k][x + ix * k] == 2 or osh == 2:
                                break
    return my_list

# 加载跳棋游戏的图片资源
# load_checkers_images()
# 开始新的游戏
start_new_game()
# 绘制棋盘
draw(-1, -1, -1, -1)
# 绑定鼠标移动事件，当鼠标移动时，调用handle_board_click函数
desk.bind("<Motion>", handle_board_click)
# 绑定鼠标点击事件，当鼠标点击时，调用handle_mouse_release函数
desk.bind("<Button-1>", handle_mouse_release)
# 开始游戏主循环
mainloop()
