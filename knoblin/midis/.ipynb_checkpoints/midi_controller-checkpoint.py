
import mido
from random import randint

class MIDIController:
    
    def __init__(self):
        print(mido.get_output_names()) # To list the output ports
        print(mido.get_input_names()) # To list the input ports

        self.outport = mido.open_output('Clarett 4Pre USB')
    
    def change_setting(self, channel, param_control_id, param_control_value, get_response=False):
            # v = randint(1,127)
            m = mido.Message(type="control_change", 
                     channel=channel, 
                     control=param_control_id, 
                     value=param_control_value)
            print("OUT: ", m)
            self.outport.send(m)

            if get_response:
                with mido.open_input() as inport:
                    for msg in inport:
                        print("IN: ", msg)
                        return msg


def knob2midi(knob_value):
    return int((127 / 10) * knob_value)


if __name__ == '__main__':
    controller = MIDIController()
    import time

    control_mapping = {
        'Drive': 11,
        'Bass': 12,
        'Mid': 13,
        'Treble': 14,
    }


    while True:
        for pnam,pci in control_mapping.items():
            pcv = knob2midi(10)
            controller.change_setting(0, pci, pcv, True)
            # controller.change_setting(1, 18, [0,127][randint(0, 1)])
            # controller.change_setting(1, 127, [0,127][randint(0, 1)])
            print()
            time.sleep(1)


