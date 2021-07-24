from static_gui_funcs import *


class ControlSetupWidget(qtw.QWidget):
    def __init__(self, player):
        super().__init__()
        self.layout = qtw.QVBoxLayout()
        self.setLayout(self.layout)

        # BattleShip button group
        self.ships_label = qtw.QLabel()
        self.ships_label.setFixedHeight(40)
        self.ships_label.setFont(qtg.QFont('monospace [Consolas]', 18))
        self.ships_label.setText('Select a ship : ')
        self.ships_label.setAlignment(qtc.Qt.AlignCenter)

        # Ship list
        self.ships_list = qtw.QWidget()
        self.ships_layout = qtw.QVBoxLayout()
        self.ships_list.setLayout(self.ships_layout)
        self.ship_button_group = qtw.QButtonGroup()
        self.add_ship_buttons(player)
        
        # Randomize button
        self.random = qtw.QPushButton('Randomize placement placement')

        # Reset button
        self.reset = qtw.QPushButton('Reset placement')

        # Done button
        self.done = qtw.QPushButton('Done')
        self.done.setFixedHeight(40)

        # Layout
        self.layout.addWidget(self.ships_label)
        self.layout.addWidget(self.ships_list)
        self.layout.addWidget(self.random)
        self.layout.addWidget(self.reset)
        self.layout.addWidget(self.done)

    def placed_ship_radio_btn(self, ship_id):
        self.ship_button_group.setExclusive(False)
        self.ship_button_group.button(ship_id).setChecked(False)
        self.ship_button_group.button(ship_id).setEnabled(False)
        self.ship_button_group.button(ship_id).setText('Placed')
        self.ship_button_group.setExclusive(True)

    def add_ship_buttons(self, player):
        """
        Creates QRadioButtons and adds them to a QButtonGroup then sets them
        in a respective layout.
        """
        for ship in player.my_ships:
            name = ship.name
            size = ship.size
            button = qtw.QRadioButton(f"{name} : Size : {size}")
            self.ships_layout.addWidget(button)
            self.ship_button_group.addButton(button, id=ship.id)
