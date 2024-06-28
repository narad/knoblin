"""GUI for Knoblin controller.

This module provides one of the two main methods for interacting with the
Knoblin controller outside of direct method calls (the other being the
command line interface).  It provides basic support for saving and changing
presets on the fly.

If running for the first time with a particular device, run the GUI prior 
to connecting knobs to servos so that they can be properly calibrated.

"""

from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, QThreadPool
from PyQt5.QtWidgets import QCheckBox, QPushButton, QFileDialog, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout


from dial import ValueDial
import sys

from servo_controller import KnobServoController
from time import sleep


class KnoblinGUI(QWidget):


    def __init__(self, n=0):
        QWidget.__init__(self)

        # Build the GUI
        layout = QGridLayout()
        self.layout = layout
        self.setLayout(layout)

        # Add title
        self.setWindowTitle("Knoblin - Graphic Controller Interface v.2")
#        self.setFixedHeight(300)
        # Set a larger fixed size for the main window
#        self.setFixedSize(800, 600)

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

        # # Debugging: Add a simple label to check visibility
        # self.debug_label = QLabel("Debug Label", self)
        # layout.addWidget(self.debug_label, 6, 0, 1, 3)

        # Add 'Show sweeps' checkbox outside the sweep options layout
        self.show_sweeps_checkbox = QCheckBox("Show sweeps")
        self.show_sweeps_checkbox.stateChanged.connect(self.toggle_sweep_options)
        self.layout.addWidget(self.show_sweeps_checkbox, 5, 0, 1, 3)

        # Setup sweep options
        self.setup_sweep_options()

        self.sweep_options_groupbox.setVisible(False)



    def setup_sweep_options(self):
        print("setting up sweep options")
        # Group Box for sweep options
        self.sweep_options_groupbox = QGroupBox("Sweep Options")
        self.sweep_options_layout = QVBoxLayout(self.sweep_options_groupbox)

        # Adjust spacing and margins
        self.sweep_options_layout.setSpacing(10)
        self.sweep_options_layout.setContentsMargins(10, 30, 10, 10)  # Increase the top margin

        # File loader for audio files
        file_loader_layout = QHBoxLayout()
        self.file_loader_button = QPushButton("Load Audio Files")
        self.file_loader_button.clicked.connect(self.load_audio_files)
        self.file_loader_button.setMaximumWidth(150)  # Control button width
        file_loader_layout.addWidget(self.file_loader_button)

        self.loaded_files_label = QLabel("No files loaded")
        file_loader_layout.addWidget(self.loaded_files_label)

        # Add file loader layout to sweep options layout
        self.sweep_options_layout.addLayout(file_loader_layout)

               # # Container Widget for sweep options
       #  self.sweep_options_widget = QWidget()
       #  self.sweep_options_layout = QVBoxLayout(self.sweep_options_widget)

        # 'Show sweeps' checkbox
        # self.show_sweeps_checkbox = QCheckBox("Show sweeps")
        # self.show_sweeps_checkbox.stateChanged.connect(self.toggle_sweep_options)
        # self.sweep_options_layout.addWidget(self.show_sweeps_checkbox)

        # # File loader for audio files
        # self.file_loader_button = QPushButton("Load Audio Files")
        # self.file_loader_button.clicked.connect(self.load_audio_files)
        # self.loaded_files_label = QLabel("No files loaded")
        # self.sweep_options_layout.addWidget(self.file_loader_button)
        # self.sweep_options_layout.addWidget(self.loaded_files_label)

        # Container for knob settings
        self.knob_settings_layout = QVBoxLayout()

        # Add the knob settings layout to the sweep options layout
        self.sweep_options_layout.addLayout(self.knob_settings_layout)


        # 'Begin Sweep' button
        self.begin_sweep_button = QPushButton("Begin Sweep")
        self.begin_sweep_button.clicked.connect(self.begin_sweep)
        self.begin_sweep_button.setMaximumWidth(150)
        self.begin_sweep_button.setEnabled(False)  # Initially disabled
        self.sweep_options_layout.addWidget(self.begin_sweep_button)

        # Add the Group Box to the main layout
        self.layout.addWidget(self.sweep_options_groupbox, 6, 0, 1, 3)


    def update_knob_info_in_sweeps(self):
        # Iterate over existing knobs to create settings inputs
        print(self.knob_settings_layout)
        for knob_info in self.knob_infos:
            print(knob_info)
            if not self.find_knob_setting_by_name(knob_info["Knob Name"]):
                self.add_knob_setting(knob_info)
#            print(self.knob_settings_layout)


    def find_knob_setting_by_name(self, knob_name):
        for i in range(self.knob_settings_layout.count()):
            # Get the layout item
            item = self.knob_settings_layout.itemAt(i)

            # Check if the item is a layout (it should be, as per your setup)
            if item.layout() is not None:
                knob_layout = item.layout()

                # Assuming the first widget in each knob layout is the QLabel for the knob name
                label_item = knob_layout.itemAt(0)
                if label_item is not None and label_item.widget() is not None:
                    label = label_item.widget()
                    if isinstance(label, QLabel) and label.text() == knob_name:
                        return True  # Found the knob with the matching name

        return False  # No matching knob name found


    def get_knob_sweep_settings(self):
        sweep_settings = {}

        for i in range(self.knob_settings_layout.count()):
            item = self.knob_settings_layout.itemAt(i)
            if item.layout() is not None:
                knob_layout = item.layout()

                # Initialize variables
                knob_name = None
                settings = {'min': None, 'max': None, 'interval': None}
                setting_keys = iter(settings.keys())  # Iterator for the settings keys

                for j in range(knob_layout.count()):
                    layout_item = knob_layout.itemAt(j)
                    if layout_item is not None:
                        widget = layout_item.widget()
                        if widget is not None:
                            if isinstance(widget, QLabel) and knob_name is None:
                                knob_name = widget.text()  # Extract the knob name
                        else:
                            qhb = layout_item.layout()
                            for k in range(qhb.count()):
                                sub_qhb = qhb.itemAt(k).widget()
                                if isinstance(sub_qhb, QComboBox):
                                    setting_key = next(setting_keys, None)
                                    if setting_key:
                                        settings[setting_key] = float(sub_qhb.currentText())

                if knob_name:
                    sweep_settings[knob_name] = settings

        return sweep_settings




    def toggle_sweep_options(self):
        print("toggling sweep options")
        show = self.show_sweeps_checkbox.isChecked()

        # Toggle the visibility of the entire group box
        self.sweep_options_groupbox.setVisible(show)

#        self.sweep_options_layout.setVisible(show)
#        self.setup_sweep_options()

        # Adjust the size of the main window based on its contents
        self.adjustSize()

        # print(show)
        # self.setup_sweep_options()
        # for i in range(self.sweep_options_layout.count()): 
        #     widget = self.sweep_options_layout.itemAt(i).widget()
        #     if widget is not None:
        #         widget.setVisible(show)


    def load_audio_files(self):
        # File dialog to load audio files
        files, _ = QFileDialog.getOpenFileNames(self, "Select Audio Files", "", "Audio Files (*.mp3 *.wav)")
        if files:
            self.loaded_files_label.setText("\n".join(files))
            self.audio_file_paths = files  # Store the file paths
            self.begin_sweep_button.setEnabled(True)  # Enable the Begin Sweep button



    def add_knob_setting(self, knob_info):
        # Vertical layout for each knob's settings
        knob_vertical_layout = QVBoxLayout()

        # Label for the knob name
        knob_label = QLabel(knob_info['Knob Name'])
        knob_vertical_layout.addWidget(knob_label)

        def create_labeled_dropdown(label_text, values, current_value):
            layout = QHBoxLayout()

            # Create and add the label
            label = QLabel(label_text)
            label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # Align label vertically center
            layout.addWidget(label)

            # Create and add the dropdown
            dropdown = QComboBox()
            dropdown.addItems(values)
            dropdown.setCurrentText(str(current_value))
            dropdown.setMaximumWidth(80)
            dropdown.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)  # Adjust size policy
            layout.addWidget(dropdown)
            layout.setAlignment(dropdown, Qt.AlignVCenter)  # Align dropdown vertically center

            # Add a stretchable space to push label and dropdown to the left
            layout.addStretch(1)

            return layout


        # Add min, max, and interval dropdowns
        min_values = self.generate_range_values(0, 10, 0.5)
        max_values = self.generate_range_values(0, 10, 0.5)
        interval_values = self.generate_range_values(0, 10, 0.1)
        knob_vertical_layout.addLayout(create_labeled_dropdown("Min:", min_values, knob_info['Min Value']))
        knob_vertical_layout.addLayout(create_labeled_dropdown("Max:", max_values, knob_info['Max Value']))
        knob_vertical_layout.addLayout(create_labeled_dropdown("Interval:", interval_values, "1.0"))  # Replace "1.0" with your default interval value

        # Add the knob's vertical layout to the main knob settings layout
        self.knob_settings_layout.addLayout(knob_vertical_layout)


    def generate_range_values(self, r_start, r_end, r_interval):
        # Generate a list of values for the dropdowns
        vals = []
        while r_start <= r_end:
            vals.append(f"{r_start:.1f}")
            r_start += r_interval
        return vals
#        return [f"{(x * 1.0):.1f}" for x in range(r_start, r_end, r_interval)]  # Adjust range as needed


    def begin_sweep(self):
        print("Beginning sweep...")

        # Load audio data for all selected WAV files
        import soundfile as sf
        input_audios = []
        sample_rate = None
        for file_path in self.audio_file_paths:
            print(file_path)
            data, sr = sf.read(file_path, dtype='float32')
            input_audios.append(data)
            sample_rate = sr
        print(sample_rate)

#        audio_data = [self.load_audio(file_path) for file_path in self.audio_file_paths]

        sweep_settings = self.get_knob_sweep_settings()
        print(sweep_settings)

        # Iterate over the knob settings layouts to get the sweep settings
        knob_names = list(sweep_settings.keys())
        print(knob_names)
        settings = [[]]
        for knob_name in knob_names:
            new_settings = []
            knob_settings = sweep_settings[knob_name]
            v = knob_settings['min']
            print(v)
            while v <= knob_settings['max']:
                print(v)
                for s in settings:
                    new_settings.append(s + [v])
                v += knob_settings['interval']
            settings = new_settings

        print(len(settings))
        print(settings)
        print("done")

        # Setup for recording loop
        from play_record import Recorder
        recorder = Recorder()

        # Perform the sweep for each knob
        fi = 0
        for setting in settings:
            for i,v in enumerate(setting):
                # Update the knob value in the GUI and servo controller
                self.dials[i].setValue(v)
                self.change_knob(i)

                # Wait for a set time
                sleep(5)  # Adjust sleep duration as needed
#                        pstring = '_'.join([f"{k}-{v}" for k,v in setting.items()])

                for input_audio in input_audios:
                    recording = recorder.record(input_audio, sr=sample_rate, filename=f"{fi}.wav")
                fi += 1




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
        self.presets_box.currentIndexChanged.connect(self.change_preset)
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

            d.dial.valueChanged.connect(lambda val, i=i: self.change_knob(i))

            # d.valueChanged.connect(lambda val, i=i: self.change_knob(i))

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

            # Update the knob info for the sweeps section
            self.update_knob_info_in_sweeps()



    def change_knob(self, i):
        """
        Changes the position of the dial with position i.  If changing to an
        invalid position, changes the color of the dial to indicate it.
        
        Args:
            i (int): the index of the dial to change
        Returns:
            bool: None
        """
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


    def change_knob_color(self, dial: ValueDial, color: str) -> None:
        """
        Changes the stylesheet of the dial, changing its color.
        
        Args:
            dial (ValueDial): the dial to change
            color (str): the color to change it to
        Returns:
            None
        """
        dial.setStyleSheet("QDial {\n"
                                "\n"
                                "background-color:" + color + ";\n"
                                "\n"
                                "}"
                        )


    def change_preset(self):
        """
        Changes the preset to the currently selected element in self.presets_box.

        Returns:
            None
        """
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
        """
        Moves all servos to their specified calibration points.
        
        Returns:
            None
        """
        print("=================================")
        self.controller.move_to_calibration()
        for dial, info in zip(self.dials, self.knob_infos):
            dial.blockSignals(True)
            if info['Attachment'] == 'max':
                dial.setValue(info['Max Value'])
            elif info['Attachment'] == 'min':
                dial.setValue(info['Min Value'])
            else: # centered
                dial.setValue(int((info['Max Value'] - info['Min Value']) / 2))
            dial.blockSignals(False)



    def save_preset(self):
        """
        Saves the position of all knobs as a preset, adding it to the dropbox of selectable presets.
        
        Returns:
            None
        """
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




