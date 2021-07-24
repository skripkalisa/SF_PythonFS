from random import randint
import os
import time

HORIZONTAL = 0
VERTICAL = 1
BOARD_SIZE = 9
legend = '''
-------------------
  Приветсвуем вас  
      в игре       
    морской бой    
-------------------
 формат ввода: x y 
 x - номер строки  
 y - номер столбца 
--------------------
'''

dashes = "-"*20


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску!"


class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"


class BoardWrongShipException(BoardException):
    def __str__(self):
        return "Корабль размещён неверно"


class Ship:
    def __init__(self, bow, ship_size, ship_vert_hor):
        self.bow = bow
        self.ship_size = ship_size
        self.ship_vert_hor = ship_vert_hor
        self.lives = ship_size

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.ship_size):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.ship_vert_hor == HORIZONTAL:
                cur_x += i

            elif self.ship_vert_hor == VERTICAL:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    def shooten(self, shot):
        return shot in self.dots


class Board:
    def __init__(self, hid=False, size=BOARD_SIZE):
        self.size = size
        self.hid = hid

        self.count = 0

        self.field = [["O"]*size for _ in range(size)]

        self.occupied = []
        self.ships = []

    def add_ship(self, ship):

        for d in ship.dots:
            if self.out(d) or d in self.occupied:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.occupied.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not(self.out(cur)) and cur not in self.occupied:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.occupied.append(cur)

    def __str__(self):
        res = ""
        board_top = [f' {i} |' for i in range(1, BOARD_SIZE+1)]
        board_top_str = ""
        for b_top in board_top:
            board_top_str += b_top
        res += "  |" + board_top_str
        # res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i+1} | " + " | ".join(row) + " |"

        if self.hid:
            res = res.replace("■", "O")
        return res

    def out(self, d):
        return not((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.occupied:
            raise BoardUsedException()

        self.occupied.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль ранен!")
                    return True

        self.field[d.x][d.y] = "."
        print("Мимо!")
        return False

    def begin(self):
        self.occupied = []


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        d = Dot(randint(0, BOARD_SIZE - 1), randint(0, BOARD_SIZE - 1))
        print(f"Ход компьютера: {d.x+1} {d.y+1}")
        return d


class User(Player):
    def ask(self):
        while True:
            coords = input("Ваш ход: ").split()

            if len(coords) != 2:
                print(" Введите 2 координаты! ")
                continue

            x, y = coords

            if not(x.isdigit()) or not(y.isdigit()):
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Dot(x-1, y-1)


class Game:
    def __init__(self, size=BOARD_SIZE):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        ship_sizes = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for ship_size in ship_sizes:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(
                    0, self.size)), ship_size, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def greet(self):
        os.system('clear')
        print(legend)

        time.sleep(1)

    def loop(self):
        num = 0
        while True:
            os.system('clear')
            # os.system('cls') # для Windows
            print(legend)
            print(dashes)
            print("Доска пользователя:")
            print(self.us.board)
            print("-"*20)
            print("Доска компьютера:")
            print(self.ai.board)
            if num % 2 == 0:
                print(dashes)
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print(dashes)
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print(dashes)
                print("Пользователь выиграл!")
                break

            if self.us.board.count == 7:
                print(dashes)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()
