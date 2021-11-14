from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, QThreadPool

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

        # Set size hints for rows
        layout.setRowStretch(1, 1)
        layout.setRowStretch(2, 1)
        layout.setRowStretch(3, 2)
        layout.setRowStretch(4, 1)

        # and size hints for cols
        for i in range(3):
            layout.setColumnMinimumWidth(i, 120)


        # Setup back-end
        self.controller = KnobServoController()

        # global vars
        self.knob_row = 3
        self.dials = []
        self.knob_infos = []
        self.presets = dict()

        # Pool for multi-threading the back-end processes
        self.threadpool = QThreadPool()



    def add_main_buttons(self, layout, row=1):
        # Add buttons to top row
        add_knob_button = QPushButton("Add Knob")
        add_knob_button.clicked.connect(self.add_dial)
        layout.addWidget(add_knob_button, row, 0, 1, 1)
        # Button to center servos
        calibrate_button = QPushButton("Calibrate Servos")
        calibrate_button.setToolTip('Move all servos to their attachment position.')
        calibrate_button.clicked.connect(self.calibrate_servos)
        layout.addWidget(calibrate_button, row, 1, 1, 1)
        # Button to save a preset
        preset_button = QPushButton("Save Preset")
        preset_button.setEnabled(False)
        preset_button.clicked.connect(self.save_preset)
        layout.addWidget(preset_button, row, 2, 1, 1)
        self.preset_button = preset_button


    def add_preset_row(self, layout, row=2):
        preset_label = QLabel("Load Preset:", self)
        preset_label.setAlignment(Qt.AlignRight)
        layout.addWidget(preset_label, row, 0, 1, 1)
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

        dialog = KnobDialog(num_knobs=len(self.dials))
        dialog.setStyleSheet(self.styleSheet())
        if dialog.exec():
            knob_name, knob_type, min_val, max_val, servo_type, attachment = dialog.getInputs()

            d = ValueDial() #QDial()
            d.setMinimum(min_val)
            d.setMaximum(max_val)
            d.setFixedWidth(80)
            d.setValue(int((max_val - min_val) / 2))

            d.valueChanged.connect(lambda val, i=i: self.change_knob(i))

            self.dials.append(d)

            self.layout.addWidget(d, self.knob_row, i, 1, 1)
            self.layout.setColumnMinimumWidth(len(self.dials), 120)

            self.knob_infos.append({
                'Knob Name': knob_name,
                'Knob Type': knob_type,
                'Min Value': min_val, 
                'Max Value': max_val,
                'Servo': servo_type,
                'Attachment': attachment
                })


            l = QLabel(knob_name.center(20), self)
            l.setFixedWidth(80)
            l.setAlignment(Qt.AlignVCenter)
            self.layout.addWidget(l, self.knob_row+1, i, 1, 1)

            # Add the corresponding knob in the controller
            self.controller.add_knob(knob_name,
                                     knob_type,
                                     servo_id = len(self.dials)-1,
                                     min_position=min_val,
                                     max_position=max_val,
                                     attachment=attachment)

            # Allow for presets to be saved
            self.preset_button.setEnabled(True)



    def change_knob(self, i):
        print("=================================")
        print(i)
        self.dials[i].value()
        info = self.knob_infos[i]
        self.controller.move(info['Knob Name'],
                             self.dials[i].value())
        print(f"Dial {i} value = {self.dials[i].value()}")
        if self.controller.is_valid(info['Knob Name'], self.dials[i].value()):
            self.change_knob_color(self.dials[i], 'white')
        else:
            self.change_knob_color(self.dials[i], 'red')


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


    def change_preset(self, i):
        print("=================================")
        if len(self.presets) > 1:
            found_preset = self.presets[self.presets_box.currentText()]
            print(found_preset)
            self.controller.move_all(found_preset)
            for knob_name, knob_value in self.presets[self.presets_box.currentText()].items():
                # self.controller.move(knob_name, knob_value)
#                sleep(2)
                # Have to get the dial ID, not great indexes for this
                did = [i for i in range(len(self.dials)) if self.knob_infos[i]['Knob Name'] == knob_name][0]
                self.dials[did].blockSignals(True)
                self.dials[did].setValue(knob_value)
                self.dials[did].blockSignals(False)


    def calibrate_servos(self):
        print("=================================")
        self.controller.move_to_calibration()
#         name2pos = { info['Knob Name']: 5 for info in self.knob_infos }
# #        cmd_list = [(info['Knob Name'], 350) for info in self.knob_infos]
#         self.controller.move_all(name2pos)
        for dial, info in zip(self.dials, self.knob_infos):
            dial.blockSignals(True)
            if info['Attachment'] == 'max':
                dial.setValue(info['Max Value'])
            elif info['Attachment'] == 'min':
                dial.setValue(info['Min Value'])
            else: # centered
                dial.setValue(int((info['Max Value'] - info['Min Value']) / 2))
            dial.blockSignals(False)


        # self.controller.center_knobs()
        # self.controller.center_knobs()


    def save_preset(self):
        if len(self.dials) > 0:
            name, ok = QInputDialog.getText(self, 'Add Preset', 'Name for Preset:')
            if ok:
                settings = { self.knob_infos[i]['Knob Name']: self.dials[i].value() for i in range(len(self.dials)) }
                print(settings)
                self.presets[name] = settings
                self.presets_box.addItems([name])
                self.presets_box.setCurrentIndex(len(self.presets)-1)





class KnobDialog(QDialog):

    def __init__(self, parent=None, num_knobs=0):
        super().__init__(parent)
        
        # Knob Name
        self.knob_name = QLineEdit(self)
        self.knob_name.setText(f"Knob {num_knobs+1}")

        # Minimum Knob Value
        self.min_value = QLineEdit(self)
        self.min_value.setToolTip('The minimum value (lowest position) of the knob.')
        self.min_value.setText("0")

        # Maximum Knob Value
        self.max_value = QLineEdit(self)
        self.max_value.setToolTip('The maximum value (highest position) of the knob.')
        self.max_value.setText("10")

        # Validators so only Int can be entered
        self.min_value.setValidator(QtGui.QIntValidator())
        self.max_value.setValidator(QtGui.QIntValidator())
#        self.safety_margin.setValidator(QtGui.QIntValidator(0,30))

        self.knob_type = QComboBox(self)
        self.knob_type.setToolTip('The type of servo being attached to this knob.')
        self.knob_type.addItems([
            "270",
            "280",
            "290",
            "300",
            "310",
            "320"
        ])
        self.knob_type.setCurrentIndex(3)

        self.servo_type = QComboBox(self)
        self.servo_type.setToolTip('The type of servo being attached to this knob.')
        self.servo_type.addItems([
#            "180", 
            "270"
        ])

        self.servo_attach = QComboBox(self)
        self.servo_attach.setToolTip('Alignment point between knob and servo.  Both devices should be in this position during attachment.')
        self.servo_attach.addItems([
            "max", 
            "center",
            "min"
        ])
        self.servo_attach.setCurrentIndex(0)


        self.safety_margin = QComboBox(self)
        self.safety_margin.setToolTip('Degree of margin between the min/max position of the servo and what it is physically capable of (can prevent over-turning the knob when servo is beyond spec).')
        self.safety_margin.addItems([
            "0", 
            "5",
            "10",
            "15",
            "20"
        ])

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self);

        layout = QFormLayout(self)
        layout.addRow("Knob Name", self.knob_name)
        layout.addRow("Minimum Value", self.min_value)
        layout.addRow("Maximum Value", self.max_value)
        layout.addRow("Knob Type", self.knob_type)
        layout.addRow("Servo Type", self.servo_type)
        layout.addRow("Servo Attachment", self.servo_attach)
        layout.addRow("Safety Margin", self.safety_margin)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    def getInputs(self):
        return (self.knob_name.text(),
                int(self.knob_type.currentText()),
                int(self.min_value.text()),
                int(self.max_value.text()),
                int(self.servo_type.currentText()),
                self.servo_attach.currentText())



if __name__ == '__main__':
    app = QApplication(sys.argv)
    knoblinGUI = KnoblinGUI()
    # Add stylesheet
    with open("css/dark.css","r") as fh:
        knoblinGUI.setStyleSheet(fh.read())
    # Show App
    knoblinGUI.show()
    sys.exit(app.exec_())




