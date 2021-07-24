from static_gui_funcs import *


class TrackingGridWidget(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = qtw.QGridLayout()
        self.setLayout(self.layout)
        self.ship_rect_tracking_obj = []

        # PC tracking Widget
        self.pc_tracking_group = qtw.QButtonGroup(self)
        self.pc_tracking_grid_widget = qtw.QWidget()
        self.pc_tracking_layout = qtw.QGridLayout()
        self.pc_tracking_grid_widget.setLayout(self.pc_tracking_layout)
        add_buttons(self.pc_tracking_layout, True, self.pc_tracking_group)
        self.pc_tracking_group.setExclusive(False)

        # PC label
        self.pc_label = qtw.QLabel()
        self.pc_label.setText('PC:')
        self.pc_label.setFont(qtg.QFont('Impact', 16))
        self.pc_label.setAlignment(qtc.Qt.AlignCenter)

        # Layout for widget
        self.layout.addWidget(self.pc_label, 0, 1)
        self.layout.addWidget(self.pc_tracking_grid_widget, 2, 1)
        add_horizontal_coordinates_label(self.layout, 1, 1)
        add_vertical_coordinates_label(self.layout, 2, 0)

    def draw_rect_tracking_grid(self, qp):
        for rect in self.ship_rect_tracking_obj:
            pos1 = [rect[0].x(), rect[0].y()]
            pos2 = [rect[1].x(), rect[1].y()]

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

    def get_rect_tracking_grid(self, my_ships):
        button_list = []
        for i in my_ships:
            if i.alive is False:
                loc_list = [i.location[0][0:2],
                            i.location[-1][0:2]]

                sub_list = []
                for k in loc_list:
                    button = grid_to_gid(k)
                    button = self.pc_tracking_group.button(button)
                    sub_list.append(button)

                button_list.append(sub_list)
        self.ship_rect_tracking_obj = button_list

    def paintEvent(self, event):
        qp = qtg.QPainter()
        qp.begin(self)
        self.draw_rect_tracking_grid(qp)
        qp.end()
