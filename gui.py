from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt

from dial import ValueDial
import sys

class Window(QWidget):
    def __init__(self, n=0):
        QWidget.__init__(self)
        layout = QGridLayout()
        self.layout = layout
        self.setLayout(layout)

        field_names = ['Knob Name', 'Min Value', 'Max Value']
        self.fields = dict()
        for col, fn in enumerate(field_names):
            # Field on top row
            f = QLineEdit(self)
            f.setFixedWidth(80)
            layout.addWidget(f, 1, col, 1, 1)

            # Label on second row
            l = QLabel(fn, self)
            l.setFixedWidth(80)
            layout.addWidget(l, 2, col, 1, 1)

            self.fields[fn] = f

        # Servo selector
        col = len(field_names)+1
        cb = QComboBox()
        cb.addItems(["180", "270", "360"])
        self.fields['Servo'] = cb
        layout.addWidget(cb, 1, col, 1, 1)
        l = QLabel("Servo", self)
        l.setFixedWidth(80)
        layout.addWidget(l, 2, col, 1, 1)

        # Set default min/max
        self.fields['Min Value'].setText("1")
        self.fields['Max Value'].setText("11")

        # Third Row, Button to add a knob
        row = 3
        self.button = QPushButton('Add Knob')
        self.button.clicked.connect(self.add_dial)
        layout.addWidget(self.button, 1, len(field_names)+2, 1, 1)

        self.knob_row = row + 1
        self.dials = []
        self.degrees = []
        self.knob_infos = []


    def add_dial(self):
        i = len(self.dials)

        # Extract vals from QLineEdits
        name = self.fields['Knob Name'].text()
        if name != "":
            minv = int(self.fields['Min Value'].text())
            maxv = int(self.fields['Max Value'].text())

            d = ValueDial() #QDial()
            d.setMinimum(minv)
            d.setMaximum(maxv)
            d.setFixedWidth(80)

            self.knob_infos.append({
                'Knob Name': name, 
                'Min Value': minv, 
                'Max Value': maxv,
                'Servo': self.fields['Servo'].currentText()
                })
            d.valueChanged.connect(lambda val, i=i: self.sliderMoved(i))
            self.dials.append(d)
            self.layout.addWidget(d, self.knob_row, i, 1, 1)

            l = QLabel(name.center(20), self)
            l.setFixedWidth(80)
            l.setAlignment(Qt.AlignVCenter)
            self.layout.addWidget(l, self.knob_row+1, i, 1, 1)
            self.fields['Knob Name'].setText("")



    def sliderMoved(self, i):
        print(i)
        print(f"Dial {i} value = {self.dials[i].value()}")
        if self.is_valid_position(i):
            self.change_knob_color(self.dials[i], 'white')
        else:
            self.change_knob_color(self.dials[i], 'red')


    def is_valid_position(self, knob_index):
        info = self.knob_infos[knob_index]



    def change_knob_color(self, knob, color):
        knob.setStyleSheet("QDial {\n"
                                "\n"
                                "background-color:" + color + ";\n"
                                "\n"
                                "}"
                        )

if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = Window()
    screen.show()
    sys.exit(app.exec_())