from static_gui_funcs import *


class PlayerGridWidget(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = qtw.QGridLayout()
        self.setLayout(self.layout)
        self.ship_rect_obj = []
        self.end_loc = []
        self.anchor_obj = None
        self.anchor_point = []

        # Player : name label
        self.player_label = qtw.QLabel()
        self.player_label.setFont(qtg.QFont('Impact', 16))
        self.player_label.setText('Your grid : ')
        self.player_label.setAlignment(qtc.Qt.AlignCenter)

        # ButtonGroup
        self.button_grid_widget = qtw.QWidget()
        self.button_grid_layout = qtw.QGridLayout()
        self.button_grid_widget.setLayout(self.button_grid_layout)
        self.player_group = qtw.QButtonGroup()
        add_buttons(self.button_grid_layout, False, self.player_group)

        # Layout
        self.layout.addWidget(self.player_label, 0, 1)
        self.layout.addWidget(self.button_grid_widget, 2, 1)
        add_horizontal_coordinates_label(self.layout, 1, 1)
        add_vertical_coordinates_label(self.layout, 2, 0)

    def is_free_grid(self, selected_button, grid):
        button_id = self.player_group.id(selected_button)
        grid_loc = gid_to_grid(button_id)

        if grid[grid_loc[0], grid_loc[1]] == 555:
            return True
        else:
            return False

    def clear_anchor(self):
        self.anchor_point = []
        self.end_loc = []
        self.update()

    def paintEvent(self, event):
        qp = qtg.QPainter()
        qp.begin(self)
        self.draw_rect(qp)
        qp.end()

    def draw_rect(self, qp):
        for rect in self.ship_rect_obj:
            pos1 = [rect[0].pos().x(), rect[0].pos().y()]
            pos2 = [rect[1].pos().x(), rect[1].pos().y()]

            qp.setPen(qtg.QPen(qtc.Qt.black, 8, qtc.Qt.SolidLine))
            width = pos2[0] - pos1[0]
            height = pos2[1] - pos1[1]

            if height == 0:
                height = 45
                if width > 0:
                    qp.drawRect(pos1[0] + 43, pos1[1] + 75, width + 65,
                                height)
                else:
                    qp.drawRect(pos1[0] + 108, pos1[1] + 75, width - 65,
                                height)
            elif width == 0:
                width = 60
                if height > 0:
                    qp.drawRect(pos1[0] + 45, pos1[1] + 75, width, height +
                                45)
                else:
                    qp.drawRect(pos1[0] + 45, pos1[1] + 123, width, height -
                                45)
