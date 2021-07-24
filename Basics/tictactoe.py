import os
import random
import time

board = [' ' for i in range(10)]
player = 1
Win = 3
Draw = 9
isOn = 0
Game = isOn
Mark = 'X'
legend = "Игрок 1 [X] --- Игрок 2 [O]\n"

# Функции

foo = " %c | %c | %c "
bar = "---|---|---"


def DrawBoard():
    for i in range(1, 4):
        print(foo % (board[3*i-2], board[3*i-1], board[3*i]))
        if i < 3:
            print(bar)
    print("")


def CheckPosition(x):
    if(board[x] == ' ' and x != 0):
        return True
    else:
        return False


def make_move(choice):
    while(not CheckPosition(choice)):
        choice = int(
            input("Введите число в промежутке [1-9] (клетки нумеруются с верхней левой) : "))
    return choice


def choose_player2(player_2):
    while(player_2 < 1 or player_2 > 2):
        os.system('clear')
        player_2 = int(
            input("Чтобы сыграть с компьютером введите '1'. Чтобы сыграть с человеком введите '2': "))
    return player_2


def CheckWin():

    global Game

    for i in range(1, 4):
        # print(f'Hor and vert lines check {i}')  # - отладка
        if (board[3*i-2] == board[3*i-1] == board[3*i] != ' '):
            Game = Win
        if (board[i] == board[i+3] == board[1+6] != ' '):
            Game = Win

    arr = []
    for i in range(1, 10, 4):
        arr.append(board[i])
    # print(f"Diag check 1{arr}")  # - отладка
    if (arr[0] == arr[1] == arr[2] != ' '):
        Game = Win

    arr = []
    for i in range(3, 8, 2):
        arr.append(board[i])
    # print(f"Diag check 2 {arr}") # - отладка
    if (arr[0] == arr[1] == arr[2] != ' '):
        Game = Win

    draw_arr = []
    for i in range(1, 10):
        draw_arr.append(board[i])
    # print(f"Draw check {draw_arr}") # - отладка
    if(' ' not in draw_arr):
        Game = Draw


# Выбираем, с кем играть
player_2 = choose_player2(0)


# Начинаем игру
while(Game == isOn):
    os.system('clear')
    # os.system('cls') # для Windows
    print(legend)
    DrawBoard()
    if(player % 2 != 0):
        print("Ходят крестики - игрок 1")
        Mark = 'X'
        choice = make_move(0)
    else:
        print("Ходят нолики - игрок 2")
        Mark = 'O'
        if player_2 == 1:
            time.sleep(random.uniform(0.0, 1))
            choice = random.randint(1, 9)
            while (not CheckPosition(choice)):
                choice = random.randint(1, 9)
                CheckPosition(choice)
        else:
            choice = make_move(0)
    board[choice] = Mark
    CheckWin()
    player += 1

os.system('clear')
# os.system('cls') # для Windows
print(legend)
DrawBoard()
if(Game == Draw):
    print("Ничья!")
elif(Game == Win):
    if(player % 2 == 0):
        print("Победил игрок 1 - крестики")
    else:
        print("Победил игрок 2 - нолики")
