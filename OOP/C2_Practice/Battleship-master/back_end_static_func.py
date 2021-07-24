import pandas as pd


def intro_text():
    print("Welcome To the classic game of battleship!")
    print("By Peter Agalakov")
    print('v0.1')


def to_dataframe(grid):
    col = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    row = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    grid = pd.DataFrame(grid, row, columns=col, dtype="Int64")
    return grid


def grid_to_gid(gird_loc):
    """ grid  """
    gid = 100 + int(str(gird_loc[0]) + str(gird_loc[1]))
    return gid


def gid_to_grid(gid):
    button_id = str(gid)
    button_id = [int(button_id[1]), int(button_id[2])]
    return button_id


def valid_entry(entry):
    """
    Checks if an entry is a valid one.
    """
    valid_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    condition_a = entry[0] in valid_list
    if len(entry) == 2:
        try:
            condition_b = 1 <= int(entry[1]) <= 10
        except ValueError as e:
            print(e)
            return False

    elif len(entry) == 3:
        try:
            condition_b = int(entry[1]) == 1 and int(entry[2]) == 0
        except ValueError as e:
            print(e)
            return False
    else:
        return False

    if condition_a and condition_b:
        return True
    else:
        return False


def valid_end_entry(end_loc, max_end_points, valid_end_loc):
    while True:
        try:
            if 0 <= int(end_loc) <= max_end_points:
                end_loc = valid_end_loc[int(end_loc)]
                return [True, end_loc]
            else:
                print('Invalid entry, please try again!')
                return [False]
        except ValueError as e:
            print(e)
            return [False]


def to_alpha_numeric(entry):

    """
    Transforms a grid position into a matrix position.
    :param entry: [3, 2]
    :return: ["C3"]
    """
    grid_dict = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G',
            7: 'H', 8: 'I', 9: 'J'}
    # Columns then rows
    entry = [grid_dict[entry[1]] + str(entry[0] + 1)]
    return entry


def to_numeric(entry):
    """
    Transforms a grid position into a matrix position
    :param entry: ["A3"]
    :return: [2, 0]
    """
    grid_dict = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6,
                 'H': 7, 'I': 8, 'J': 9}
    # Columns then rows
    if len(entry) == 2:
        entry = [int(entry[1]) - 1, grid_dict[entry[0]]]
    elif len(entry) == 3:
        entry = [9, grid_dict[entry[0]]]

    return entry


def select_dict(a_list):
    """
    Takes a list of valid locations and make a dictionary with them so the
    user can easily select an end location.
    :param a_list:
    :return: {dict}
    """

    my_dict_print = []
    for i in a_list:
        my_dict_print += to_alpha_numeric(i)
    return a_list, my_dict_print


def place_ship_on_grid(ship, start, end):
    """
    Once a start location and an end location was selected, do the
    actual placement on the players grid. Changes the state from 0 to 1
    on the matrix in-place.
    :param ship: object
    :param start: list []
    :param end: list []
    :return: In-place
    """
    if start == end:
        ship.location = [[start[0], start[1], 1]]
        return

    vertical = abs(end[0] - start[0])
    horizontal = abs(end[1] - start[1])
    step = 1
    if (end[1] - start[1]) < 0 or (end[0] - start[0]) < 0:
        step *= -1

    if horizontal > 0:
        fixed_column = start[0]
        for i in range(start[1], end[1] + step, step):
            ship.location += [[fixed_column, i, 1]]

    if vertical > 0:
        fixed_column = start[1]
        for i in range(start[0], end[0] + step, step):
            ship.location += [[i, fixed_column, 1]]


def get_salvo(ship_objects):
    """
    Receives a list of ship object, counts how may ships are alive and return
    its equivalent value in salvos.
    :param [ship_objects,..]
    :return: int
    """
    salvo = 0
    for i in ship_objects:
        if i.alive is True:
            salvo += 1
    return salvo


