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
    alpha = float('inf')
    beta = float('-inf')
    return alpha,beta

# 定义选择游戏难度的回调函数-普通
def select_difficulty_hard():
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
n2_list = ()  
ur = 3  
k_rez = 0  
o_rez = 0
poz1_x = -1  
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
def draw(x_poz_1, y_poz_1, x_poz_2, y_poz_2): 
    global field
    global red_border, green_border
    k = 100
    x = 0
    desk.delete('all')
    red_border = desk.create_rectangle(-5, -5, -5, -5, outline="red", width=5)
    green_border = desk.create_rectangle(-5, -5, -5, -5, outline="green", width=5)

    while x < 8 * k:
        y = 1 * k
        while y < 8 * k:
            desk.create_rectangle(x, y, x + k, y + k, fill="black")
            y += 2 * k
        x += 2 * k
    x = 1 * k

    while x < 8 * k:
        y = 0
        while y < 8 * k:
            desk.create_rectangle(x, y, x + k, y + k, fill="black")
            y += 2 * k
        x += 2 * k

    for y in range(8):
        for x in range(8):
            z = field[y][x]
            if z:
                if (x_poz_1, y_poz_1) != (x, y):
                    color = 'black' if z in [1,2] else 'white'
                    desk.create_oval(x*k+5, y*k+5, (x+1)*k-5, (y+1)*k-5, fill=color, outline='#6E7B8B', width=7)
                    if z in [2,4]:
                        # Set king outline color
                        color_king = 'red'
                        desk.create_oval(x*k+5, y*k+5, (x+1)*k-5, (y+1)*k-5, fill=color, outline=color_king, width=7)

    z = field[y_poz_1][x_poz_1]
    if z:
        color = 'black' if z in [1, 2] else 'white'
        desk.create_oval(x_poz_1*k+5, y_poz_1*k+5, (x_poz_1+1)*k-5, (y_poz_1+1)*k-5, fill=color, outline='#6E7B8B', width=7 ,tag='ani')

    kx = 1 if x_poz_1 < x_poz_2 else -1
    ky = 1 if y_poz_1 < y_poz_2 else -1
    for kk in range(abs(x_poz_1 - x_poz_2)):
        for ii in range(33):
            desk.move('ani', 3 * kx, 3 * ky)
            desk.update()
            time.sleep(0.01)

# 显示游戏结束的消息，并询问玩家是否要开始新游戏
def message(s):
    global is_player_move, i
    z = 'Игра завершена'
    if s == 1:
        i = messagebox.askyesno(title=z, message='Вы победили!\nНажми "Да" что бы начать заново.', icon='info')
    if s == 2:
        i = messagebox.askyesno(title=z, message='Вы проиграли!\nНажми "Да" что бы начать заново.', icon='info')
    if s == 3:
        i = messagebox.askyesno(title=z, message='Ходов больше нет.\nНажми "Да" что бы начать заново.', icon='info')
    if i:
        start_new_game()
        draw(-1, -1, -1, -1)
        is_player_move = True

# 玩家点击棋盘时的处理函数
def position_1(event):
    x, y = event.x // 100, event.y // 100
    desk.coords(green_border, x * 100, y * 100, x * 100 + 100, y * 100 + 100)

# 玩家释放鼠标按钮时的处理函数
def position_2(event):
    global poz1_x, poz1_y, poz2_x, poz2_y
    global is_player_move
    x, y = event.x // 100, event.y // 100
    if field[y][x] == 1 or field[y][x] == 2:
        desk.coords(red_border, x * 100, y * 100, x * 100 + 100, y * 100 + 100)
        poz1_x, poz1_y = x, y
        # 检查是否有可以跳吃的棋子
        has_jump_moves = has_jump_moves_available()
        if has_jump_moves:
            print(can_piece_jump(poz1_x, poz1_y))
            if not can_piece_jump(poz1_x, poz1_y):
                messagebox.showinfo("提示", "当前有可以跳吃的棋子，请选择可以跳吃的棋子！")
    else:
        if poz1_x != -1:  # клетка выбрана
            poz2_x, poz2_y = x, y
            if is_player_move:  # ход игрока?
                player_turn()
                if not is_player_move:
                    time.sleep(0.5)
                    computer_turn()
            poz1_x = -1
            desk.coords(red_border, -5, -5, -5, -5)

# 检查是否有可以跳吃的棋子
def has_jump_moves_available():
    if len(check_moves_i1(list_hi())) > 0:
        return True
    return False

# 检查指定的棋子是否可以跳吃
def can_piece_jump(x, y):
    piece = field[y][x]
    if piece == 1 or piece == 2:
        jumps = check_moves_i1p([], x, y)
        if jumps:
            return True
    return False

# 电脑玩家的回合
def computer_turn():  
    global is_player_move
    global n2_list
    check_hk(1, (), [], alpha, beta)
    if n2_list:
        kh = len(n2_list)
        th = random.randint(0, kh - 1)
        dh = len(n2_list[th])
        for k in range(dh - 1):
            my_list = move(1, n2_list[th][k][0], n2_list[th][k][1], n2_list[th][1 + k][0], n2_list[th][1 + k][1])
        n2_list = []
        is_player_move = True

    s_k, s_i = scan()
    if not s_i:
        message(2)
    elif not s_k:
        message(1)
    elif is_player_move and not (list_hi()):
        message(3)
    elif not is_player_move and not (list_hk()):
        message(3)

# list_hk函数用于获取电脑玩家的所有可能的移动
def list_hk():
    # 首先尝试获取所有可以吃掉对手棋子的移动
    my_list = check_moves_k1([])  
    # 如果没有可以吃掉对手棋子的移动，那么获取所有普通的移动
    if not my_list:
        my_list = check_moves_k2p([])
    return my_list

# check_hk函数用于评估电脑玩家的所有可能的移动
def check_hk(tur, n_list, my_list, alpha, beta):  
    global field
    global n2_list
    global l_rez, k_rez, o_rez
    if not my_list:  
        my_list = list_hk()  

    if my_list:
        k_pole = copy.deepcopy(field)
        for ((poz1_x, poz1_y), (poz2_x, poz2_y)) in my_list:  
            t_list = move(0, poz1_x, poz1_y, poz2_x, poz2_y)
            if t_list:  
                check_hk(tur, (n_list + ((poz1_x, poz1_y),)), t_list, alpha, beta)
            else:
                check_hi(tur, [], alpha, beta)
                if tur == 1:
                    t_rez = o_rez / k_rez
                    if not n2_list:  
                        n2_list = (n_list + ((poz1_x, poz1_y), (poz2_x, poz2_y)),)
                        l_rez = t_rez  
                        alpha = max(alpha, t_rez)
                    else:
                        if t_rez == l_rez:
                            n2_list = n2_list + (n_list + ((poz1_x, poz1_y), (poz2_x, poz2_y)),)
                        if t_rez > l_rez:
                            n2_list = ()
                            n2_list = (n_list + ((poz1_x, poz1_y), (poz2_x, poz2_y)),)
                            l_rez = t_rez  
                            alpha = max(alpha, t_rez)
                    o_rez = 0
                    k_rez = 0

            field = copy.deepcopy(k_pole)  
            if beta <= alpha:
                break
    else: 
        s_k, s_i = scan()
        o_rez += (s_k - s_i)
        k_rez += 1

# list_hi函数用于获取人类玩家的所有可能的移动
def list_hi():
    # 首先尝试获取所有可以吃掉对手棋子的移动
    my_list = check_moves_i1([])  
    # 如果没有可以吃掉对手棋子的移动，那么获取所有普通的移动
    if not my_list:
        my_list = check_moves_i2([])  # здесь проверяем оставшиеся ходы
    return my_list

# check_hi函数用于评估人类玩家的所有可能的移动
def check_hi(tur, my_list, alpha, beta):
    global field, k_rez, o_rez
    global ur
    if not my_list:
        my_list = list_hi()

    if my_list:  
        k_pole = copy.deepcopy(field)
        for ((poz1_x, poz1_y), (poz2_x, poz2_y)) in my_list:
            t_list = move(0, poz1_x, poz1_y, poz2_x, poz2_y)
            if t_list:  
                check_hi(tur, t_list, alpha, beta)
            else:
                if tur < ur:
                    check_hk(tur + 1, (), [], alpha, beta)
                else:
                    s_k, s_i = scan()  
                    o_rez += (s_k - s_i)
                    k_rez += 1
                    beta = min(beta, o_rez / k_rez)

            field = copy.deepcopy(k_pole)  
            if beta <= alpha:
                break
    else:  
        s_k, s_i = scan()  
        o_rez += (s_k - s_i)
        k_rez += 1
        beta = min(beta, o_rez / k_rez)

# scan函数用于扫描棋盘，统计双方的棋子数量
def scan():  
    global field
    # 人类玩家的棋子数量
    s_i = 0
    # 电脑玩家的棋子数量
    s_k = 0
    # 遍历棋盘
    for k in range(8):
        for ii in field[k]:
            # 根据棋子的类型，更新双方的棋子数量
            if ii == 1:
                s_i += 1
            if ii == 2:
                s_i += 3
            if ii == 3:
                s_k += 1
            if ii == 4:
                s_k += 3
    return s_k, s_i

# player_turn函数用于处理人类玩家的回合
def player_turn():
    global poz1_x, poz1_y, poz2_x, poz2_y
    global is_player_move
    is_player_move = False  
    # 获取人类玩家的所有可能的移动
    my_list = list_hi()
    if my_list:
        # 如果人类玩家选择的移动在所有可能的移动中，那么执行这个移动
        if ((poz1_x, poz1_y), (poz2_x, poz2_y)) in my_list:
            t_list = move(1, poz1_x, poz1_y, poz2_x, poz2_y)  
            if t_list:  
                is_player_move = True  
        else:
            is_player_move = True  
    # 更新棋盘
    desk.update()  

# move函数用于执行一次移动
def move(f, poz1_x, poz1_y, poz2_x, poz2_y):
    global field
    # 如果是人类玩家的回合，那么在界面上画出这次移动
    if f: draw(poz1_x, poz1_y, poz2_x, poz2_y)  
    # 如果人类玩家的棋子到达了对方的基地，那么升级这个棋子
    if poz2_y == 0 and field[poz1_y][poz1_x] == 1:
        field[poz1_y][poz1_x] = 2
    # 如果电脑玩家的棋子到达了对方的基地，那么升级这个棋子
    if poz2_y == 7 and field[poz1_y][poz1_x] == 3:
        field[poz1_y][poz1_x] = 4
    # 更新棋盘
    field[poz2_y][poz2_x] = field[poz1_y][poz1_x]
    field[poz1_y][poz1_x] = 0

    # 计算移动的方向
    kx = ky = 1
    if poz1_x < poz2_x:
        kx = -1
    if poz1_y < poz2_y:
        ky = -1
    x_poz, y_poz = poz2_x, poz2_y
    # 如果在移动的过程中吃掉了对方的棋子，那么更新棋盘，并检查是否可以继续吃掉对方的棋子
    while (poz1_x != x_poz) or (poz1_y != y_poz):
        x_poz += kx
        y_poz += ky
        if field[y_poz][x_poz] != 0:
            field[y_poz][x_poz] = 0
            if f:
                draw(-1, -1, -1, -1)  
            if field[poz2_y][poz2_x] == 3 or field[poz2_y][poz2_x] == 4:
                return check_moves_k1p([], poz2_x, poz2_y)
            elif field[poz2_y][poz2_x] == 1 or field[poz2_y][poz2_x] == 2:
                return check_moves_i1p([], poz2_x, poz2_y)
    if f:
        draw(poz1_x, poz1_y, poz2_x, poz2_y)

# check_moves_k1函数用于检查电脑玩家的所有棋子的所有可能的吃子移动
def check_moves_k1(my_list):  
    for y in range(8): 
        for x in range(8):
            # 检查每个棋子的所有可能的吃子移动
            my_list = check_moves_k1p(my_list, x, y)
    return my_list

# check_moves_k1p函数用于检查一个棋子的所有可能的吃子移动
def check_moves_k1p(my_list, x, y):
    # 如果这个棋子是电脑玩家的普通棋子
    if field[y][x] == 3:
        # 检查所有可能的吃子方向
        for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
            # 如果吃子的方向是合法的，并且可以吃掉人类玩家的棋子
            if 0 <= y + iy + iy <= 7 and 0 <= x + ix + ix <= 7:
                if field[y + iy][x + ix] == 1 or field[y + iy][x + ix] == 2:
                    if field[y + iy + iy][x + ix + ix] == 0:
                        # 添加这个吃子移动到列表中
                        my_list.append(((x, y), (x + ix + ix, y + iy + iy)))
    # 如果这个棋子是电脑玩家的王棋
    if field[y][x] == 4:  
        for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
            osh = 0  
            for k in range(1, 8):
                if 0 <= y + iy * k <= 7 and 0 <= x + ix * k <= 7:
                    if osh == 1:
                        # 添加这个吃子移动到列表中
                        my_list.append(((x, y), (x + ix * k, y + iy * k)))
                    if field[y + iy * k][x + ix * k] == 1 or field[y + iy * k][x + ix * k] == 2:
                        osh += 1
                    if field[y + iy * k][x + ix * k] == 3 or field[y + iy * k][x + ix * k] == 4 or osh == 2:
                        if osh > 0:
                            # 如果不能吃子，那么删除这个移动
                            my_list.pop()
                        break
    return my_list

# check_moves_k2p函数用于检查电脑玩家的所有棋子的所有可能的非吃子移动
def check_moves_k2p(my_list):
    for y in range(8):
        for x in range(8):
            # 如果这个棋子是电脑玩家的普通棋子
            if field[y][x] == 3:
                # 检查所有可能的非吃子方向
                for ix, iy in (-1, 1), (1, 1):
                    if 0 <= y + iy <= 7 and 0 <= x + ix <= 7:
                        # 如果这个方向是空的，那么可以移动
                        if field[y + iy][x + ix] == 0:
                            my_list.append(((x, y), (x + ix, y + iy)))
                        # 如果这个方向是人类玩家的棋子，那么可以吃子
                        if field[y + iy][x + ix] == 1 or field[y + iy][x + ix] == 2:
                            if 0 <= y + iy * 2 <= 7 and 0 <= x + ix * 2 <= 7:
                                if field[y + iy * 2][x + ix * 2] == 0:
                                    my_list.append(((x, y), (
                                        x + ix * 2, y + iy * 2)))
            # 如果这个棋子是电脑玩家的王棋
            if field[y][x] == 4:
                # 检查所有可能的非吃子方向
                for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
                    osh = 0
                    for k in range(1, 8):
                        if 0 <= y + iy * k <= 7 and 0 <= x + ix * k <= 7:
                            # 如果这个方向是空的，那么可以移动
                            if field[y + iy * k][x + ix * k] == 0:
                                my_list.append(((x, y), (x + ix * k, y + iy * k)))
                            # 如果这个方向是人类玩家的棋子，那么可以吃子
                            if field[y + iy * k][x + ix * k] == 1 or field[y + iy * k][x + ix * k] == 2:
                                osh += 1
                            # 如果这个方向是电脑玩家的棋子，那么不能移动
                            if field[y + iy * k][x + ix * k] == 3 or field[y + iy * k][x + ix * k] == 4 or osh == 2:
                                break
    return my_list

# check_moves_i1函数用于检查人类玩家的所有棋子的所有可能的吃子移动
def check_moves_i1(my_list):
    my_list = []
    for y in range(8):
        for x in range(8):
            # 检查每个棋子的所有可能的吃子移动
            my_list = check_moves_i1p(my_list, x, y)
    return my_list

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
# 绑定鼠标移动事件，当鼠标移动时，调用position_1函数
desk.bind("<Motion>", position_1)
# 绑定鼠标点击事件，当鼠标点击时，调用position_2函数
desk.bind("<Button-1>", position_2)
# 开始游戏主循环
mainloop()
