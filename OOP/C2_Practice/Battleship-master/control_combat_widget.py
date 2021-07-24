from static_gui_funcs import *


class ControlCombatWidget(qtw.QWidget):
    def __init__(self):
        super().__init__()
        ########
        # initialization
        ########
        self.layout = qtw.QVBoxLayout()
        self.setLayout(self.layout)

        # Fire button
        self.fire_button = qtw.QPushButton('Fire the Missiles')
        self.fire_button.setFixedHeight(60)

        # LCD num
        self.salvo_label = qtw.QLabel('Available salvos:')
        self.salvo_lcd = qtw.QLCDNumber()

        # Layout
        self.layout.addWidget(self.fire_button)
        self.layout.addWidget(self.salvo_label)
        self.layout.addSpacing(100)
        self.layout.addWidget(self.salvo_lcd)
