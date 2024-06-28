
import mido
from random import randint

class MIDIController:
    
    def __init__(self):
        print(mido.get_output_names()) # To list the output ports
        print(mido.get_input_names()) # To list the input ports
        self.outport = mido.open_output('Clarett 4Pre USB')

    def change_setting(self, channel, param_control_id, param_control_value, verbose=False, get_response=False):
            m = mido.Message(type="control_change", 
                     channel=channel, 
                     control=param_control_id, 
                     value=param_control_value)
            if verbose:
                print("OUT: ", m)
            self.outport.send(m)

            if get_response:
                with mido.open_input() as inport:
                    for msg in inport:
                        if verbose:
                            print("IN: ", msg)
                        return msg

    def change_preset(self, channel, program):
        m = mido.Message(type="program_change", 
                         channel=channel, 
                         program=program)     
        self.outport.send(m)


if __name__ == '__main__':
    import sys
    m = MIDIController()
    m.change_preset(channel=0, program=int(sys.argv[1]))


