"""
The central servo controller module.

This module instantiates a connection with an Arduino unit, serves as
a interface for creating virtual knobs, and sends messages to update
the physical knob positions.
"""

import serial   
from util.connect_arduino import get_port_name
from knob import Knob, ActuatedKnob
from servo import Servo270
from time import sleep

from typing import Dict, List


class KnobServoController:

    def __init__(self, knobs: List[ActuatedKnob]=[], port_name: str=None) -> None:
        # Acquire port ID
        if port_name is None:
            port_name = get_port_name()

        # Setup Arduino/Serial connection
        self.arduino = serial.Serial(port_name, 9600)

        # Create indexes
        self.name2knob = { knob.name : knob for knob in knobs }
        self.id2knob = { knob.servo.servo_id : knob for knob in knobs }


    def knobs(self):
        """
        Changes the preset to the currently selected element in self.presets_box.

        Returns:
            list[ActuatedKnob]: a list of current knobs
        """
        return [self.id2knob[i] for i in range(self.num_knobs())]


    def num_knobs(self):
        """
        Returns the number of knobs currently known by the controller.

        Returns:
            int: the number of knobs
        """
        return len(self.id2knob)


    def add_knob(self, knob_name: str, knob_type: int, servo_id: int, min_position: int, max_position: int, attachment: str) -> None:
        """
        Create a new ActuatedKnob and add it to the controller

        Returns:
            None
        """
        knob = Knob(knob_name,
                    knob_type,
                    min_position,
                    max_position)
        servo = Servo270(servo_id)
        aknob = ActuatedKnob(knob=knob,
                             servo=servo,
                             attachment=attachment)
        self.name2knob[knob_name] = aknob
        self.id2knob[servo.servo_id] = aknob


    def move(self, knob_name: str, position: int, delay:int=0) -> None:
        self.move_all({knob_name: position})


    def move_all(self, name2pos: Dict[str,int], delay:int=0) -> None:
        print(name2pos)
        cmd_str = ""
        for i in range(len(self.id2knob)):
            knob = self.id2knob[i]
            try:
                pos = name2pos[knob.name]
                cmd_code = knob.command_from_position(pos)
            except:
                cmd_code = 0
            print(cmd_code)
            cmd_str += f"{cmd_code:03}"
        print(cmd_str)
        print()
        self.arduino.write(cmd_str.encode())


    def move_to_calibration(self):
        print("in move to calib")
        print(self.knobs())
        name2pos = {}
        for knob in self.knobs():
            print("  ", knob.name)
            name2pos[knob.name] = knob.calibration_position()
        print("calibration dict: ", name2pos)
        self.move_all(name2pos)


    def is_valid(self, knob_name, position):
        return self.name2knob[knob_name].is_valid(position)

