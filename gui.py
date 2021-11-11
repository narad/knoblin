from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt

from dial import ValueDial
import sys

from knobs.servo_controller import KnobServoController
from time import sleep


class KnoblinGUI(QWidget):


    def __init__(self, n=0):
        QWidget.__init__(self)

        # Build the GUI
        layout = QGridLayout()
        self.layout = layout
        self.setLayout(layout)

        # Add title
        self.setWindowTitle("Knoblin - Graphic Controller Interface v.1")
        self.setFixedHeight(300)

        # Add elements
        self.add_menu()
        self.add_main_buttons(layout, row=1)
        self.add_preset_row(layout, row=2)

        # Set size hints
        layout.setRowStretch(1, 1)
        layout.setRowStretch(2, 1)
        layout.setRowStretch(3, 2)
        layout.setRowStretch(4, 1)

        # Setup back-end
        self.controller = KnobServoController()

        # global vars
        self.knob_row = 3
        self.dials = []
        self.knob_infos = []
        self.presets = dict()


    def add_main_buttons(self, layout, row=1):
        # Add buttons to top row
        center_button = QPushButton("Add Knob")
        center_button.clicked.connect(self.add_dial)
        layout.addWidget(center_button, row, 0, 1, 1)
        # Button to center servos
        center_button = QPushButton("Center Servos")
        center_button.clicked.connect(self.center_servos)
        layout.addWidget(center_button, row, 1, 1, 1)
        # Button to save a preset
        center_button = QPushButton("Save Preset")
        center_button.clicked.connect(self.save_preset)
        layout.addWidget(center_button, row, 2, 1, 1)


    def add_preset_row(self, layout, row=2):
        layout.addWidget(QLabel("Load Preset:", self), row, 0, 1, 1)
        # Dropdown select
        self.presets_box = QComboBox(self)
        self.presets_box.currentIndexChanged.connect(lambda val: self.change_preset(val))
        layout.addWidget(self.presets_box, row, 1, 1, 1)       


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
        dialog.setStyleSheet(self.styleSheet())
        if dialog.exec():
            name, min_val, max_val, servo_type = dialog.getInputs()
            min_val = int(min_val)
            max_val = int(max_val)

            d = ValueDial() #QDial()
            d.setMinimum(min_val)
            d.setMaximum(max_val)
            d.setFixedWidth(80)

            self.knob_infos.append({
                'Knob Name': name, 
                'Min Value': min_val, 
                'Max Value': max_val,
                'Servo': servo_type
                })
            d.valueChanged.connect(lambda val, i=i: self.change_knob(i))
            self.dials.append(d)
            self.layout.addWidget(d, self.knob_row, i, 1, 1)

            l = QLabel(name.center(20), self)
            l.setFixedWidth(80)
            l.setAlignment(Qt.AlignVCenter)
            self.layout.addWidget(l, self.knob_row+1, i, 1, 1)

            # Add the corresponding knob in the controller
            self.controller.add_knob(name,
                                     servo_id = len(self.dials)-1,
                                     min_position=min_val,
                                     max_position=max_val)



    def change_knob(self, i):
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


    def change_preset(self, i):
        if len(self.presets) > 1:
            for knob_name, knob_value in self.presets[self.presets_box.currentText()]:
                self.controller.move(knob_name, knob_value)
                sleep(2)
                # Have to get the dial ID, not great indexes for this
                did = [i for i in range(len(self.dials)) if self.knob_infos[i]['Knob Name'] == knob_name][0]
                self.dials[did].setValue(knob_value)



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
        for dial in self.dials:
            dial.center()

        self.controller.center_knobs()
        self.controller.center_knobs()


    def save_preset(self):
        name, ok = QInputDialog.getText(self, 'Add Preset', 'Name for Preset:')
        if ok:
            settings = [(self.knob_infos[i]['Knob Name'], self.dials[i].value()) for i in range(len(self.dials))]
            print(settings)
            self.presets[name] = settings
            self.presets_box.addItems([name])
            self.presets_box.setCurrentIndex(len(self.presets)-1)





class KnobDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

#        self.setStyleSheet(stylesheet)
        
        self.knob_name = QLineEdit(self)
        self.min_value = QLineEdit(self)
        self.max_value = QLineEdit(self)
        self.safety_margin = QLineEdit(self)

        # Validators so only int can be entered
        self.min_value.setValidator(QtGui.QIntValidator())
        self.max_value.setValidator(QtGui.QIntValidator())
        self.safety_margin.setValidator(QtGui.QIntValidator(0,30))

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
        layout.addRow("Safety Margin", self.safety_margin)
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
    knoblinGUI = KnoblinGUI()
    # Add stylesheet
    with open("css/dark.css","r") as fh:
        knoblinGUI.setStyleSheet(fh.read())
    # Show App
    knoblinGUI.show()
    sys.exit(app.exec_())













        # layout.setRowStretch(0, 1)
        # layout.setRowStretch(1, 1)
        # layout.setRowStretch(2, 3)
#        layout.setRowStretch(4, 3)


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

