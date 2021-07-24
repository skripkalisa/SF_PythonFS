import sys
from back_end import Player, Pc
from static_gui_funcs import *
from tracking_grid_wdiget import TrackingGridWidget
from player_grid_widget import PlayerGridWidget
from control_setup_widget import ControlSetupWidget
from control_combat_widget import ControlCombatWidget
import random


class SplashScreen(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = qtw.QVBoxLayout()
        self.setLayout(self.layout)

        # Heading label
        self.heading = qtw.QLabel()
        self.heading.setText('You sunk my BattleShip!!')
        self.layout.addWidget(self.heading)
        heading_font = qtg.QFont('Impact', 18, qtg.QFont.Bold)
        heading_font.setStretch(qtg.QFont.ExtraExpanded)
        self.heading.setFont(heading_font)

        # Logo
        self.logo = qtg.QPixmap('pic/battleship_icon.png')
        self.logo_label = qtw.QLabel()
        self.logo_label.setPixmap(self.logo)
        self.layout.addWidget(self.logo_label)

        # Start and quit buttons
        self.start_btn = qtw.QPushButton('New Round')
        self.quit_btn = qtw.QPushButton('Quit')
        self.layout.addWidget(self.start_btn)
        self.layout.addWidget(self.quit_btn)

        # About
        self.footing = qtw.QLabel()
        self.footing.setText('V0.1 By Peter Agalakov')
        self.footing.setAlignment(qtc.Qt.AlignCenter)
        self.layout.addWidget(self.footing)

        # Logic
        self.start_btn.clicked.connect(self.start_setup)
        self.quit_btn.clicked.connect(self.quit_now)

        # Frame settings
        self.setWindowTitle("BattleShip!")
        self.center()
        self.show()

    def quit_now(self):
        self.close()
        sys.exit()

    def start_setup(self):
        global setup
        setup = Setup()
        setup.show()
        self.hide()

    def center(self):
        qr = self.frameGeometry()
        cp = qtw.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class Combat(qtw.QWidget):
    def __init__(self, setup_obj):
        super().__init__()
        ########
        # initialization
        ########
        self.selected_locations = []
        self.combat_layout = qtw.QGridLayout()
        self.setLayout(self.combat_layout)
        self.setup_obj = setup_obj
        self.pc = Pc('Pc')
        self.TGW = TrackingGridWidget()
        self.CCW = ControlCombatWidget()
        self.PGW = self.setup_obj.PGW
        self.selected_limit = self.setup_obj.player.get_salvo_limit()

        ########
        # Logic
        ########
        self.CCW.fire_button.clicked.connect(self.fire_button_action)
        self.CCW.salvo_lcd.display(str(self.selected_limit))

        ########
        # Messages
        ########
        self.win_msg = qtw.QMessageBox()
        self.win_msg.setText('You Win! :)')
        self.win_msg.setIcon(qtw.QMessageBox.Information)

        self.lose_msg = qtw.QMessageBox()
        self.lose_msg.setText('You Lose! :(')
        self.lose_msg.setIcon(qtw.QMessageBox.Information)

        self.too_many_selected_msg = qtw.QMessageBox()
        self.too_many_selected_msg.setText('Too many locations selected')
        self.too_many_selected_msg.setIcon(qtw.QMessageBox.Critical)

        ########
        # Layout
        ########

        # Adding all Widgets to main grid layout
        self.combat_layout.addWidget(self.PGW, 0, 1)
        self.combat_layout.addWidget(self.TGW, 0, 2)
        self.combat_layout.addWidget(self.CCW, 0, 3)
        self.combat_layout.addWidget(self.setup_obj.console_label, 1, 1)

        ########
        # Logic
        ########
        self.setup_to_combat()
        self.TGW.pc_tracking_group.buttonClicked.connect(
            self.grid_space_selected)
        self.who_starts = random.randint(1, 2)
        if self.who_starts == 2:
            print('PC goes first')
            self.play_a_turn()

        ########
        # Window settings
        ########
        self.update_combat_interface()
        self.move(200, 200)
        self.setWindowTitle("BattleShip!")

    ########
    # obj funcs
    ########
    def grid_space_selected(self, btn_obj):
        if btn_obj.isChecked():
            self.selected_limit -= 1
            self.check_limit()
            self.CCW.salvo_lcd.display(str(self.selected_limit))
            self.selected_locations.append(
                    self.TGW.pc_tracking_group.id(btn_obj))

        elif btn_obj.isChecked() is False:
            self.selected_limit += 1
            self.check_limit()
            self.CCW.salvo_lcd.display(str(self.selected_limit))
            self.selected_locations.remove(
                self.TGW.pc_tracking_group.id(btn_obj))

    def fire_button_action(self):
        """ Logic for the fire button """
        if self.selected_limit >= 0:
            for i in self.selected_locations:
                loc = gid_to_grid(i)
                fire_salvo(self.pc, loc, self.setup_obj.player)

            self.check_winner()
            self.pc.is_alive()
            self.play_a_turn()
            self.check_winner()
            self.setup_obj.player.is_alive()
            self.selected_locations = []
            self.selected_limit = self.setup_obj.player.get_salvo_limit()
            self.check_limit()
            self.CCW.salvo_lcd.display(str(self.selected_limit))
            self.TGW.get_rect_tracking_grid(self.pc.my_ships)
            self.update_combat_interface()
            self.update()

        else:
            self.too_many_selected_msg.exec()

    def setup_to_combat(self):
        """Disables the buttons in the player gird"""
        for button_id in range(100, 200, 1):
            button = self.setup_obj.PGW.player_group.button(button_id)
            button.setEnabled(False)

    def play_a_turn(self):
        hit_list = self.pc.make_hit_list(self.pc.get_salvo_limit())
        for i in hit_list:
            fire_salvo(self.setup_obj.player, i, self.pc)
        self.update_combat_interface()

    def update_combat_interface(self):
        """ Updates both player gird and tracking gird"""
        update_interface_gird_values_combat(self.setup_obj.PGW.player_group,
                                            self.setup_obj.player.grid)

        update_interface_gird_values_combat(
                                        self.TGW.pc_tracking_group,
                                        self.setup_obj.player.tracking_grid)

    def check_limit(self):
        if self.selected_limit <= 0:
            disable_salvo_selection(self.TGW.pc_tracking_group,
                                    self.setup_obj.player.tracking_grid, True)
        elif self.selected_limit > 0:
            disable_salvo_selection(self.TGW.pc_tracking_group,
                                    self.setup_obj.player.tracking_grid, False)

    def check_winner(self):
        if self.setup_obj.player.get_salvo_limit() == 0:
            self.lose_msg.exec()
            splash.show()
            self.close()

        elif self.pc.get_salvo_limit() == 0:
            self.win_msg.exec()
            splash.show()
            self.close()


class Setup(qtw.QWidget):
    def __init__(self):
        super().__init__()
        ########
        # initialization
        ########

        self.player = Player('Player')
        self.PGW = PlayerGridWidget()
        self.CSW = ControlSetupWidget(self.player)

        # Main Layout
        self.layout = qtw.QGridLayout()
        self.setLayout(self.layout)

        # Warning label
        self.console_label = qtw.QLabel()
        self.console_label.setText('Please set up your ships.')
        self.console_label.setAlignment(qtc.Qt.AlignCenter)
        self.console_label.setFont(qtg.QFont('monospace [Consolas]', 14))

        ########
        # Logic
        ########
        self.reset_ship_list()

        # Player gird button connect
        self.PGW.player_group.buttonClicked.connect(
            self.setup_button_click)

        # Random push button connect
        self.CSW.random.clicked.connect(self.randomize_ships)

        # Rest push button connect
        self.CSW.reset.clicked.connect(self.reset_ship_list)

        # Done push button connect
        self.CSW.done.clicked.connect(self.setup_done)
        self.CSW.ship_button_group.buttonClicked.connect(self.PGW.clear_anchor)

        ########
        # Layout
        ########
        self.layout.addWidget(self.PGW, 0, 0)
        self.layout.addWidget(self.CSW, 0, 1)
        self.layout.addWidget(self.console_label, 1, 0)

        ########
        # Window settings
        ########
        update_interface_gird_values_setup(self.PGW,
                                           self.player.grid,
                                           False)
        self.center()
        self.setWindowTitle("BattleShip!")

    ########
    # obj funcs
    ########
    def setup_button_click(self, button_obj):
        ship_obj = None
        ship_id = self.CSW.ship_button_group.checkedId()

        # Check if a ship is selected for placement
        if ship_id != -1:
            ship_obj = self.player.get_ship_by_id(ship_id)
        else:
            self.console_label.setText('No ship is selected')
            self.console_label.setStyleSheet("background-color: #ffa500")
            return

        # Check if the button pressed is part of a valid end location and if
        # the button is free to use
        end_point_check = self.end_point_in_end_loc(button_obj)
        is_grid_free = self.PGW.is_free_grid(button_obj, self.player.grid)

        # Check if location in use.
        if is_grid_free is False:
            self.console_label.setText('Location is used!')
            self.console_label.setStyleSheet("background-color: #ffa500")
            self.PGW.anchor_point = []
            self.PGW.end_loc = []

        # Check the user clicked on an end point with an anchor point present.
        elif end_point_check:
            self.player.place_ship(ship_obj,
                                   self.PGW.anchor_obj,
                                   button_obj,
                                   self.PGW.player_group)

            self.PGW.ship_rect_obj.append([self.PGW.anchor_obj,
                                          button_obj])

            self.console_label.setStyleSheet("background-color: #00ffa5")
            self.console_label.setText(ship_obj.name + " has been placed")
            self.CSW.placed_ship_radio_btn(ship_id)
            self.PGW.anchor_point = []
            self.PGW.end_loc = []

        # Check if space is free to set an anchor point.
        elif is_grid_free:
            self.PGW.end_loc, print_loc = self.get_end_loc(button_obj,
                                                       ship_obj)
            self.PGW.anchor_obj = button_obj
            self.console_label.setText(str(print_loc))
            self.console_label.setStyleSheet("background-color: #00ffa5")

        update_interface_gird_values_setup(self.PGW, self.player.grid, False)
        self.update()

    def get_end_loc(self, selected_button, ship):
        selected_button = self.PGW.player_group.id(selected_button)
        start_loc = gid_to_grid(selected_button)

        return self.player.set_anchor(ship, start_loc)

    def end_point_in_end_loc(self, selected_button):
        selected_button = self.PGW.player_group.id(selected_button)
        selected_button = gid_to_grid(selected_button)
        for i in self.PGW.end_loc:
            if i == selected_button:
                return True
        else:
            return False

    def reset_ship_list(self):
        csw = self.CSW
        ship_list_reset_text(csw, self.player.my_ships)
        csw.ship_button_group.setExclusive(False)
        for i in csw.ship_button_group.buttons():
            i.setChecked(False)
            i.setEnabled(True)
        csw.ship_button_group.setExclusive(True)
        self.player = Player('Player')
        self.PGW.anchor_point = []
        self.PGW.end_loc = []
        self.PGW.ship_rect_obj = []
        self.update()
        self.console_label.setText('Board was reset')
        self.console_label.setStyleSheet("background-color: #00ffa5")
        update_interface_gird_values_setup(self.PGW,
                                           self.player.grid,
                                           True)

    def setup_done(self):
        global combat

        all_ships_placed = True
        for i in self.player.my_ships:
            if not i.location:
                all_ships_placed = False

        if all_ships_placed:
            combat = Combat(self)
            self.hide()
            combat.show()
        else:
            msg_box = qtw.QMessageBox()
            msg_box.setIcon(qtw.QMessageBox.Warning)
            msg_box.setText('You need to place all ships')
            msg_box.exec()

    def center(self):
        qr = self.frameGeometry()
        cp = qtw.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def randomize_ships(self):
        self.reset_ship_list()
        self.player.randomize_ships()

        for i in range(1, 8, 1):
            self.CSW.placed_ship_radio_btn(i)

        self.get_list_randomized()
        self.update()
        update_interface_gird_values_setup(self.PGW, self.player.grid, False)

    def get_list_randomized(self):
        loc_list = []
        for j in self.player.my_ships:
            loc_list.append([j.location[0][0:2],
                             j.location[-1][0:2]])

        button_list = []
        for k in loc_list:
            sub_list = []
            for g in k:
                button = grid_to_gid(g)
                button = self.PGW.player_group.button(button)
                sub_list.append(button)
            button_list.append(sub_list)
        self.PGW.ship_rect_obj = button_list


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    splash = SplashScreen()
    setup = None
    combat = None
    sys.exit(app.exec())
