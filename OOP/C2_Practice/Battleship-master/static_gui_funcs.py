from back_end_static_func import *

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc


def disable_salvo_selection(group, grid, disable):
    """Updates interface of a buttongroup with a grid"""

    for button_id in range(100, 200, 1):
        button_str = str(button_id)
        y = int(button_str[1])
        x = int(button_str[2])
        # Makes the buttons uncheckable to begin with
        button_is_checked = group.button(button_id).isChecked()
        free = grid[y][x] == 555
        if free and not button_is_checked and disable:
            group.button(button_id).setEnabled(False)
        elif free:
            group.button(button_id).setEnabled(True)


def update_interface_gird_values_combat(group, grid):
    """Updates interface of a buttongroup with a grid"""

    for button_id in range(100, 200, 1):
        button_str = str(button_id)
        y = int(button_str[1])
        x = int(button_str[2])

        # Sets the default button background and text
        group.button(button_id).setStyleSheet(
            "background-color: #72bcd4")
        group.button(button_id).setText(
            str(grid[y][x]))

        # Makes the buttons uncheckable to begin with
        group.button(button_id).setCheckable(False)

        if grid[y][x] == 0:
            group.button(button_id).setStyleSheet(
                "background-color: red")
            group.button(button_id).setEnabled(False)
        elif grid[y][x] == 7:
            group.button(button_id).setStyleSheet(
                "background-color: #e6ae17")
            group.button(button_id).setEnabled(False)
        elif grid[y][x] == 555:
            group.button(button_id).setCheckable(True)
        elif grid[y][x] == 1:
            group.button(button_id).setStyleSheet(
                "background-color: #808080")
            group.button(button_id).setEnabled(False)


def update_interface_gird_values_setup(obj, grid, rest):
    """
    Update the grid interface during the setup phase of the game.
    """
    anchor_point = obj.player_group.id(obj.anchor_obj)

    for button_id in range(100, 200, 1):
        button_str = str(button_id)
        y = int(button_str[1])
        x = int(button_str[2])

        # Set the color of unused space to sea blue
        obj.player_group.button(button_id).setStyleSheet(
            "background-color: #72bcd4")

        # Set the color to gray for used space
        if grid[y][x] == 1:
            obj.player_group.button(button_id).setStyleSheet(
                "background-color: #808080")
        # Sets the anchor point to orange
        elif anchor_point == button_id:
            obj.player_group.button(button_id).setStyleSheet(
                "background-color: orange")

        # Reset the color when rest button is pressed.
        elif grid[y][x] == 555 and rest is True:
            obj.player_group.button(button_id).setStyleSheet(
                "background-color: #72bcd4")

        anchor_update(obj, button_id)
        end_loc_update(obj, button_id)


def end_loc_update(obj, button_id):
    """
    Updates the possible end locations in red on the players setup grid gui.
    :param obj: gui window object that has a button group
    :param button_id: the button id of the button group (int : 110)
    :return:
    """
    for loc in obj.end_loc:
        if loc == gid_to_grid(button_id):
            obj.player_group.button(button_id).setStyleSheet(
                "background-color: red")


def anchor_update(obj, button_id):
    """
    Updates the anchor point on the players setup grid gui.
    :param obj: gui window object that has a button group
    :param button_id: the button id of the button group (int : 110)
    :return:
    """
    loc = obj.anchor_point
    if loc == gid_to_grid(button_id):
        obj.player_group.button(button_id).setStyleSheet(
            "background-color: #ffa500")


def add_horizontal_coordinates_label(layout, row, col):
    """
    adds a horizontal/vertical widget with all the labels for the girds to
    a layout
    :param layout:
    :param row: row in QGridLayout
    :param col: col in QGridLayout
    :return:
    """
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    horizontal_widget = qtw.QWidget()
    horizontal_layout = qtw.QHBoxLayout()
    horizontal_widget.setLayout(horizontal_layout)
    for i in letters:
        alpha_label = qtw.QLabel(i)
        alpha_label.setAlignment(qtc.Qt.AlignCenter)
        horizontal_layout.addWidget(alpha_label)
    layout.addWidget(horizontal_widget, row, col)


def add_vertical_coordinates_label(layout, row, col):
    """
    adds a horizontal/vertical widget with all the labels for the girds to
    a layout
    :param layout:
    :param row: row in QGridLayout
    :param col: col in QGridLayout
    :return:
    """
    vertical_widget = qtw.QWidget()
    vertical_layout = qtw.QVBoxLayout()
    vertical_widget.setLayout(vertical_layout)

    for i in range(1, 11, 1):
        num_label = qtw.QLabel(str(i))
        num_label.setAlignment(qtc.Qt.AlignCenter)
        vertical_layout.addWidget(num_label)
    layout.addWidget(vertical_widget, row, col)


def add_buttons(layout, ischeckable, group):
    """
    Creates buttons and adds them to a QButtonGroup then sets them in a
    QGridLayout.
    :param layout: QGridLayout
    :param ischeckable: Bool
    :param group: QButtonGroup
    :return:
    """
    positions = [[i, j] for i in range(10) for j in range(10)]
    for position in positions:
        gid = grid_to_gid([position[0], position[1]])
        loc = str(to_alpha_numeric(position))
        loc = loc.replace("['", "")
        loc = loc.replace("']", "")
        button = qtw.QPushButton("{}".format(loc))
        button.setFixedHeight(40)
        button.setFixedWidth(60)
        button.setCheckable(ischeckable)
        layout.addWidget(button, *position)
        group.addButton(button, id=gid)


def ship_list_reset_text(obj, ships):
    """
    Resets the ship radio button text when the reset button is pressed.
    :param obj:
    :param ships:
    :return:
    """
    for ship in ships:
        name = ship.name
        size = ship.size
        obj.ship_button_group.button(ship.id).setText(
            f"{name} : \n Size : {size}")


def add_rect(obj, anchor_point_obj, end_point_obj):
    pos1 = [anchor_point_obj.pos().x(), anchor_point_obj.pos().y()]

    pos2 = [end_point_obj.pos().x(), end_point_obj.pos().y()]

    obj.ship_rect.append([pos1, pos2])
    obj.update()


def fire_salvo(obj, location, track_obj):
    """
    Fires a single salvo, checks if it was a hit or miss. Makes the
    modifications necessary in both player and pc gird.
    """
    y = location[0]
    x = location[1]
    if obj.grid[y, x] == 1:
        if obj.name != 'PC':
            print('Hit!!')
        track_obj.tracking_grid[y, x] = 0
        for i in obj.my_ships:
            for j in i.location:
                if j[0] == y and j[1] == x:
                    j[2] = 0
                    i.in_place(obj.grid)

    else:
        track_obj.tracking_grid[location[0]][location[1]] = 7
        obj.grid[location[0]][location[1]] = 7
        if obj.name != 'PC':
            print('Miss!!')
