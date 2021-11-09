from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt

from dial import ValueDial
import sys

from knobs.servo_controller import KnobServoController


class Window(QWidget):
    def __init__(self, n=0):
        QWidget.__init__(self)
        layout = QGridLayout()

        # layout.setRowStretch(0, 1)
        # layout.setRowStretch(1, 1)
        # layout.setRowStretch(2, 3)
        layout.setRowStretch(4, 3)

        self.layout = layout
        self.setLayout(layout)
        self.add_menu()
        self.controller = KnobServoController()

#         field_names = ['Knob Name', 'Min Value', 'Max Value']
#         self.fields = dict()
#         for col, fn in enumerate(field_names):
#             # Field on top row
#             f = QLineEdit(self)
#             f.setFixedWidth(80)
#             layout.addWidget(f, 1, col, 1, 1)

#             # Label on second row
#             l = QLabel(fn, self)
#             l.setFixedWidth(80)
#             layout.addWidget(l, 2, col, 1, 1)

#             self.fields[fn] = f

#         # Servo selector
#         col = len(field_names)+1
#         cb = QComboBox()
#         cb.addItems([
# #            "180", 
#             "270"
#         ])
#         self.fields['Servo'] = cb
#         layout.addWidget(cb, 1, col, 1, 1)
#         l = QLabel("Servo", self)
#         l.setFixedWidth(80)
#         layout.addWidget(l, 2, col, 1, 1)

#         # Set default min/max
#         self.fields['Min Value'].setText("1")
#         self.fields['Max Value'].setText("11")

#         # Button to add a knob on the far right of first row
#         self.button = QPushButton('Add Knob')
#         self.button.clicked.connect(self.add_dial)
#         layout.addWidget(self.button, 1, len(field_names)+2, 1, 1)

#         # Row 2 & 3 reserved for future knobs and labels


        # Add buttons to bottom row
        center_button = QPushButton("Add Knob")
        center_button.clicked.connect(self.add_dial)
        layout.addWidget(center_button, 1, 1, 1, 1)

        # Add buttons to bottom row
        center_button = QPushButton("Center Servos")
        center_button.clicked.connect(self.center_servos)
        layout.addWidget(center_button, 1, 2, 1, 1)

        self.knob_row = 3
        self.dials = []
        self.degrees = []
        self.knob_infos = []


    def add_menu(self):
        # create menu
        menubar = QMenuBar()
        self.layout.addWidget(menubar, 0, 0)
        actionFile = menubar.addMenu("File")
        actionFile.addAction("New")
        actionFile.addAction("Open")
        actionFile.addAction("Save")
        actionFile.addSeparator()
        actionFile.addAction("Quit")
        menubar.addMenu("Edit")
        menubar.addMenu("View")
        menubar.addMenu("Help")


    def add_dial(self):

        i = len(self.dials)

        dialog = KnobDialog()
        if dialog.exec():
            name, min_val, max_val, servo_type = dialog.getInputs()
            min_val = int(min_val)
            max_val = int(max_val)



        # # Extract vals from QLineEdits
        # name = self.fields['Knob Name'].text()
        # if name != "":
        #     minv = int(self.fields['Min Value'].text())
        #     maxv = int(self.fields['Max Value'].text())

            d = ValueDial() #QDial()
            d.setMinimum(min_val)
            d.setMaximum(max_val)
            d.setFixedWidth(80)

            self.knob_infos.append({
                'Knob Name': name, 
                'Min Value': min_val, 
                'Max Value': max_val,
                'Servo': servo_type #self.fields['Servo'].currentText()
                })
            d.valueChanged.connect(lambda val, i=i: self.sliderMoved(i))
            self.dials.append(d)
            self.layout.addWidget(d, self.knob_row, i, 1, 1)

            l = QLabel(name.center(20), self)
            l.setFixedWidth(80)
            l.setAlignment(Qt.AlignVCenter)
            self.layout.addWidget(l, self.knob_row+1, i, 1, 1)
#            self.fields['Knob Name'].setText("")

            # Add the corresponding knob in the controller
            self.controller.add_knob(name,
                                     servo_id = len(self.dials)-1,
                                     min_position=min_val,
                                     max_position=max_val)



    def sliderMoved(self, i):
        print(i)
        self.dials[i].value()
        info = self.knob_infos[i]
        self.controller.move(info['Knob Name'],
                             self.dials[i].value())
        print(f"Dial {i} value = {self.dials[i].value()}")
        # if self.is_valid_position(i):
        #     self.change_knob_color(self.dials[i], 'white')
        # else:
        #     self.change_knob_color(self.dials[i], 'red')


    # May implement this at some point: for when servo is 180
    # and dial position is outside servo range
    def is_valid_position(self, knob_index):
        info = self.knob_infos[knob_index]


    def change_knob_color(self, knob, color):
        knob.setStyleSheet("QDial {\n"
                                "\n"
                                "background-color:" + color + ";\n"
                                "\n"
                                "}"
                        )

    def center_servos(self):
        self.controller.center_knobs()

        # text, ok = QInputDialog().getText(self, 
        #                                   "QInputDialog().getText()",
        #                                   "User name:", QLineEdit.Normal)
        # if ok and text:
        #     textLabel.setText(text)



class KnobDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.knob_name = QLineEdit(self)
        self.min_value = QLineEdit(self)
        self.max_value = QLineEdit(self)

        cb = QComboBox(self)
        cb.addItems([
#            "180", 
            "270"
        ])
        self.servo_type = cb #QLineEdit(self)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self);

        layout = QFormLayout(self)
        layout.addRow("Knob Name", self.knob_name)
        layout.addRow("Minimum Value", self.min_value)
        layout.addRow("Maximum Value", self.max_value)
        layout.addRow("Servo Type", self.servo_type)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    def getInputs(self):
        return (self.knob_name.text(), 
                self.min_value.text(),
                self.max_value.text(),
                self.servo_type.currentText())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = Window()
    screen.setFixedHeight(300)
    screen.show()
    sys.exit(app.exec_())

