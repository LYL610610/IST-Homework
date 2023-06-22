from tkinter import *
import random
import time
import copy
from tkinter import messagebox

main_window = Tk()  # создаём окно
main_window.title('Шашки')  # заголовок окна
desk = Canvas(main_window, width=800, height=800, bg='#FFFFFF')  # создаю окно 800х800 черного цвета
desk.pack()

n2_list = ()  # конечный список ходов компьютера
ur = 3  # количество предсказываемых компьютером ходов
k_rez = 0  # !!!
o_rez = 0
poz1_x = -1  # клетка не задана
is_player_move = True  # определение хода игрока(да)


def load_checkers_images():  # загружаем изображения шашек
    global checkers
    i1 = PhotoImage(file="res/1b.gif")
    i2 = PhotoImage(file="res/1bk.gif")
    i3 = PhotoImage(file="res/1h.gif")
    i4 = PhotoImage(file="res/1hk.gif")
    checkers = [0, i1, i2, i3, i4]


def start_new_game():  # начинаем новую игру
    global field
    field = [[0, 3, 0, 3, 0, 3, 0, 3],
             [3, 0, 3, 0, 3, 0, 3, 0],
             [0, 3, 0, 3, 0, 3, 0, 3],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [1, 0, 1, 0, 1, 0, 1, 0],
             [0, 1, 0, 1, 0, 1, 0, 1],
             [1, 0, 1, 0, 1, 0, 1, 0]]


def draw(x_poz_1, y_poz_1, x_poz_2, y_poz_2):  # рисуем игровое поле
    global checkers
    global field
    global red_border, green_border
    k = 100
    x = 0
    desk.delete('all')
    red_border = desk.create_rectangle(-5, -5, -5, -5, outline="red", width=5)
    green_border = desk.create_rectangle(-5, -5, -5, -5, outline="green", width=5)

    while x < 8 * k:  # рисуем доску
        y = 1 * k
        while y < 8 * k:
            desk.create_rectangle(x, y, x + k, y + k, fill="black")
            y += 2 * k
        x += 2 * k
    x = 1 * k

    while x < 8 * k:  # рисуем доску
        y = 0
        while y < 8 * k:
            desk.create_rectangle(x, y, x + k, y + k, fill="black")
            y += 2 * k
        x += 2 * k

    for y in range(8):  # рисуем стоячие шашки
        for x in range(8):
            z = field[y][x]
            if z:
                if (x_poz_1, y_poz_1) != (x, y):  # стоячие шашки?
                    desk.create_image(x * k, y * k, anchor=NW, image=checkers[z])

    # рисуем активную шашку
    z = field[y_poz_1][x_poz_1]
    if z:  # ???
        desk.create_image(x_poz_1 * k, y_poz_1 * k, anchor=NW, image=checkers[z], tag='ani')

    # вычисление коэф. для анимации
    kx = 1 if x_poz_1 < x_poz_2 else -1
    ky = 1 if y_poz_1 < y_poz_2 else -1
    for kk in range(abs(x_poz_1 - x_poz_2)):  # анимация перемещения шашки
        for ii in range(33):
            desk.move('ani', 3 * kx, 3 * ky)
            desk.update()  # обновление
            time.sleep(0.01)


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
        draw(-1, -1, -1, -1)  # рисуем игровое поле
        is_player_move = True  # ход игрока доступен


def position_1(event):  # выбор клетки для хода 1
    x, y = event.x // 100, event.y // 100  # вычисляем координаты клетки
    desk.coords(green_border, x * 100, y * 100, x * 100 + 100, y * 100 + 100)  # рамка в выбранной клетке


def position_2(event):  # выбор клетки для хода 2
    global poz1_x, poz1_y, poz2_x, poz2_y
    global is_player_move
    x, y = event.x // 100, event.y // 100  # вычисляем координаты клетки
    if field[y][x] == 1 or field[y][x] == 2:  # проверяем шашку игрока в выбранной клетке
        desk.coords(red_border, x * 100, y * 100, x * 100 + 100, y * 100 + 100)  # рамка в выбранной клетке
        poz1_x, poz1_y = x, y
    else:
        if poz1_x != -1:  # клетка выбрана
            poz2_x, poz2_y = x, y
            if is_player_move:  # ход игрока?
                player_turn()
                if not is_player_move:
                    time.sleep(0.5)
                    computer_turn()  # передаём ход компьютеру
                    # main_window.after(500, computer_turn(0))  # !!!# передаём ход компьютеру
            poz1_x = -1  # клетка не выбрана
            desk.coords(red_border, -5, -5, -5, -5)  # рамка вне поля


def computer_turn():  # !!!
    global is_player_move
    global n2_list
    check_hk(1, (), [])
    if n2_list:  # проверяем наличие доступных ходов
        kh = len(n2_list)  # количество ходов
        th = random.randint(0, kh - 1)  # случайный ход
        dh = len(n2_list[th])  # длина хода
        for k in range(dh - 1):
            # выполняем ход
            my_list = move(1, n2_list[th][k][0], n2_list[th][k][1], n2_list[th][1 + k][0], n2_list[th][1 + k][1])
        n2_list = []  # очищаем список ходов
        is_player_move = True  # ход игрока доступен

    # определяем победителя
    s_k, s_i = scan()
    if not s_i:
        message(2)
    elif not s_k:
        message(1)
    elif is_player_move and not (list_hi()):
        message(3)
    elif not is_player_move and not (list_hk()):
        message(3)


def list_hk():  # составляем список ходов компьютера
    my_list = check_moves_k1([])  # здесь проверяем обязательные ходы
    if not my_list:
        my_list = check_moves_k2p([])  # здесь проверяем оставшиеся ходы
    return my_list


def check_hk(tur, n_list, my_list):  # !!!
    global field
    global n2_list
    global l_rez, k_rez, o_rez
    if not my_list:  # если список ходов пустой...
        my_list = list_hk()  # заполняем

    if my_list:
        k_pole = copy.deepcopy(field)  # копируем поле
        for ((poz1_x, poz1_y), (poz2_x, poz2_y)) in my_list:  # проходим все ходы по списку
            t_list = move(0, poz1_x, poz1_y, poz2_x, poz2_y)
            if t_list:  # если существует ещё ход
                check_hk(tur, (n_list + ((poz1_x, poz1_y),)), t_list)
            else:
                check_hi(tur, [])
                if tur == 1:
                    t_rez = o_rez / k_rez
                    if not n2_list:  # записыаем если пустой
                        n2_list = (n_list + ((poz1_x, poz1_y), (poz2_x, poz2_y)),)
                        l_rez = t_rez  # сохряняем наилучший результат
                    else:
                        if t_rez == l_rez:
                            n2_list = n2_list + (n_list + ((poz1_x, poz1_y), (poz2_x, poz2_y)),)
                        if t_rez > l_rez:
                            n2_list = ()
                            n2_list = (n_list + ((poz1_x, poz1_y), (poz2_x, poz2_y)),)
                            l_rez = t_rez  # сохряняем наилучший результат
                    o_rez = 0
                    k_rez = 0

            field = copy.deepcopy(k_pole)  # возвращаем поле
    else:  # ???
        s_k, s_i = scan()  # подсчёт результата хода
        o_rez += (s_k - s_i)
        k_rez += 1


def list_hi():  # составляем список ходов игрока
    my_list = check_moves_i1([])  # здесь проверяем обязательные ходы
    if not my_list:
        my_list = check_moves_i2([])  # здесь проверяем оставшиеся ходы
    return my_list


def check_hi(tur, my_list):
    global field, k_rez, o_rez
    global ur
    if not my_list:
        my_list = list_hi()

    if my_list:  # проверяем наличие доступных ходов
        k_pole = copy.deepcopy(field)  # копируем поле
        for ((poz1_x, poz1_y), (poz2_x, poz2_y)) in my_list:
            t_list = move(0, poz1_x, poz1_y, poz2_x, poz2_y)
            if t_list:  # если существует ещё ход
                check_hi(tur, t_list)
            else:
                if tur < ur:
                    check_hk(tur + 1, (), [])
                else:
                    s_k, s_i = scan()  # подсчёт результата хода
                    o_rez += (s_k - s_i)
                    k_rez += 1

            field = copy.deepcopy(k_pole)  # возвращаем поле
    else:  # доступных ходов нет
        s_k, s_i = scan()  # подсчёт результата хода
        o_rez += (s_k - s_i)
        k_rez += 1


def scan():  # подсчёт пешек на поле
    global field
    s_i = 0
    s_k = 0
    for k in range(8):
        for ii in field[k]:
            if ii == 1:
                s_i += 1
            if ii == 2:
                s_i += 3
            if ii == 3:
                s_k += 1
            if ii == 4:
                s_k += 3
    return s_k, s_i


def player_turn():
    global poz1_x, poz1_y, poz2_x, poz2_y
    global is_player_move
    is_player_move = False  # считаем ход игрока выполненным
    my_list = list_hi()
    if my_list:
        if ((poz1_x, poz1_y), (poz2_x, poz2_y)) in my_list:  # проверяем ход на соответствие правилам игры
            t_list = move(1, poz1_x, poz1_y, poz2_x, poz2_y)  # если всё хорошо, делаем ход
            if t_list:  # если есть ещё ход той же пешкой
                is_player_move = True  # считаем ход игрока невыполненным
        else:
            is_player_move = True  # считаем ход игрока невыполненным
    desk.update()  # !!!обновление


def move(f, poz1_x, poz1_y, poz2_x, poz2_y):
    global field
    if f: draw(poz1_x, poz1_y, poz2_x, poz2_y)  # рисуем игровое поле
    # превращение
    if poz2_y == 0 and field[poz1_y][poz1_x] == 1:
        field[poz1_y][poz1_x] = 2
    # превращение
    if poz2_y == 7 and field[poz1_y][poz1_x] == 3:
        field[poz1_y][poz1_x] = 4
    # делаем ход
    field[poz2_y][poz2_x] = field[poz1_y][poz1_x]
    field[poz1_y][poz1_x] = 0

    # рубим пешку игрока
    kx = ky = 1
    if poz1_x < poz2_x:
        kx = -1
    if poz1_y < poz2_y:
        ky = -1
    x_poz, y_poz = poz2_x, poz2_y
    while (poz1_x != x_poz) or (poz1_y != y_poz):
        x_poz += kx
        y_poz += ky
        if field[y_poz][x_poz] != 0:
            field[y_poz][x_poz] = 0
            if f:
                draw(-1, -1, -1, -1)  # рисуем игровое поле
            # проверяем ход той же пешкой...
            if field[poz2_y][poz2_x] == 3 or field[poz2_y][poz2_x] == 4:  # ...компьютера
                return check_moves_k1p([], poz2_x, poz2_y)  # возвращаем список доступных ходов
            elif field[poz2_y][poz2_x] == 1 or field[poz2_y][poz2_x] == 2:  # ...игрока
                return check_moves_i1p([], poz2_x, poz2_y)  # возвращаем список доступных ходов
    if f:
        draw(poz1_x, poz1_y, poz2_x, poz2_y)  # рисуем игровое поле


def check_moves_k1(my_list):  # проверка наличия обязательных ходов
    for y in range(8):  # сканируем всё поле
        for x in range(8):
            my_list = check_moves_k1p(my_list, x, y)
    return my_list


def check_moves_k1p(my_list, x, y):
    if field[y][x] == 3:  # пешка
        for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
            if 0 <= y + iy + iy <= 7 and 0 <= x + ix + ix <= 7:
                if field[y + iy][x + ix] == 1 or field[y + iy][x + ix] == 2:
                    if field[y + iy + iy][x + ix + ix] == 0:
                        my_list.append(((x, y), (x + ix + ix, y + iy + iy)))  # запись хода в конец списка
    if field[y][x] == 4:  # пешка с короной
        for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
            osh = 0  # определение правильности хода
            for k in range(1, 8):
                if 0 <= y + iy * k <= 7 and 0 <= x + ix * k <= 7:
                    if osh == 1:
                        my_list.append(((x, y), (x + ix * k, y + iy * k)))  # запись хода в конец списка
                    if field[y + iy * k][x + ix * k] == 1 or field[y + iy * k][x + ix * k] == 2:
                        osh += 1
                    if field[y + iy * k][x + ix * k] == 3 or field[y + iy * k][x + ix * k] == 4 or osh == 2:
                        if osh > 0:
                            my_list.pop()  # удаление хода из списка
                        break
    return my_list


def check_moves_k2p(my_list):  # проверка наличия остальных ходов
    for y in range(8):  # сканируем всё поле
        for x in range(8):
            if field[y][x] == 3:  # пешка
                for ix, iy in (-1, 1), (1, 1):
                    if 0 <= y + iy <= 7 and 0 <= x + ix <= 7:
                        if field[y + iy][x + ix] == 0:
                            my_list.append(((x, y), (x + ix, y + iy)))  # запись хода в конец списка
                        if field[y + iy][x + ix] == 1 or field[y + iy][x + ix] == 2:
                            if 0 <= y + iy * 2 <= 7 and 0 <= x + ix * 2 <= 7:
                                if field[y + iy * 2][x + ix * 2] == 0:
                                    my_list.append(((x, y), (
                                        x + ix * 2, y + iy * 2)))  # запись хода в конец списка
            if field[y][x] == 4:  # пешка с короной
                for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
                    osh = 0  # определение правильности хода
                    for k in range(1, 8):
                        if 0 <= y + iy * k <= 7 and 0 <= x + ix * k <= 7:
                            if field[y + iy * k][x + ix * k] == 0:
                                my_list.append(((x, y), (x + ix * k, y + iy * k)))  # запись хода в конец списка
                            if field[y + iy * k][x + ix * k] == 1 or field[y + iy * k][x + ix * k] == 2:
                                osh += 1
                            if field[y + iy * k][x + ix * k] == 3 or field[y + iy * k][x + ix * k] == 4 or osh == 2:
                                break
    return my_list


def check_moves_i1(my_list):  # проверка наличия обязательных ходов
    my_list = []  # список ходов
    for y in range(8):  # сканируем всё поле
        for x in range(8):
            my_list = check_moves_i1p(my_list, x, y)
    return my_list


def check_moves_i1p(my_list, x, y):
    if field[y][x] == 1:  # пешка
        for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
            if 0 <= y + iy + iy <= 7 and 0 <= x + ix + ix <= 7:
                if field[y + iy][x + ix] == 3 or field[y + iy][x + ix] == 4:
                    if field[y + iy + iy][x + ix + ix] == 0:
                        my_list.append(((x, y), (x + ix + ix, y + iy + iy)))  # запись хода в конец списка
    if field[y][x] == 2:  # пешка с короной
        for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
            osh = 0  # определение правильности хода
            for k in range(1, 8):
                if 0 <= y + iy * k <= 7 and 0 <= x + ix * k <= 7:
                    if osh == 1:
                        my_list.append(((x, y), (x + ix * k, y + iy * k)))  # запись хода в конец списка
                    if field[y + iy * k][x + ix * k] == 3 or field[y + iy * k][x + ix * k] == 4:
                        osh += 1
                    if field[y + iy * k][x + ix * k] == 1 or field[y + iy * k][x + ix * k] == 2 or osh == 2:
                        if osh > 0:
                            my_list.pop()  # удаление хода из списка
                        break
    return my_list


def check_moves_i2(my_list):  # проверка наличия остальных ходов
    for y in range(8):  # сканируем всё поле
        for x in range(8):
            if field[y][x] == 1:  # пешка
                for ix, iy in (-1, -1), (1, -1):
                    if 0 <= y + iy <= 7 and 0 <= x + ix <= 7:
                        if field[y + iy][x + ix] == 0:
                            my_list.append(((x, y), (x + ix, y + iy)))  # запись хода в конец списка
                        if field[y + iy][x + ix] == 3 or field[y + iy][x + ix] == 4:
                            if 0 <= y + iy * 2 <= 7 and 0 <= x + ix * 2 <= 7:
                                if field[y + iy * 2][x + ix * 2] == 0:
                                    my_list.append(((x, y), (
                                        x + ix * 2, y + iy * 2)))  # запись хода в конец списка
            if field[y][x] == 2:  # пешка с короной
                for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
                    osh = 0  # определение правильности хода
                    for k in range(1, 8):
                        if 0 <= y + iy * k <= 7 and 0 <= x + ix * k <= 7:
                            if field[y + iy * k][x + ix * k] == 0:
                                my_list.append(((x, y), (x + ix * k, y + iy * k)))  # запись хода в конец списка
                            if field[y + iy * k][x + ix * k] == 3 or field[y + iy * k][x + ix * k] == 4:
                                osh += 1
                            if field[y + iy * k][x + ix * k] == 1 or field[y + iy * k][x + ix * k] == 2 or osh == 2:
                                break
    return my_list


load_checkers_images()  # здесь загружаем изображения шашек
start_new_game()  # начинаем новую игру
draw(-1, -1, -1, -1)  # рисуем игровое поле
desk.bind("<Motion>", position_1)  # движение мышки по полю
desk.bind("<Button-1>", position_2)  # нажатие левой кнопки

mainloop()
