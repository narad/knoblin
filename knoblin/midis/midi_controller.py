
import mido
from random import randint

def knob2midi(knob_value):
    return int((127 / 10) * knob_value)


class MIDIController:
    
    def __init__(self, midi_device_name, midi_channel, midi_mapping):
        print(mido.get_output_names()) # To list the output ports
        print(mido.get_input_names()) # To list the input ports
        self.outport = mido.open_output(midi_device_name) #)
        self.midi_channel = midi_channel
        self.midi_mapping = midi_mapping
        self.last_setting = None

    def change_setting(self, setting):
        # for pnam, pci in control_mapping.items():
        for pname, pval in setting.items():
            if self.last_setting is not None and setting[pname] == last_setting[pname]:
                continue
            else:
                if args.verbose:
                    print(pname, "\t", pval)
                external_cid = self.control_mapping[pname]
                pci =  self.midi_mapping[external_cid]
                pcv = knob2midi(int(pval * 10))
                if args.verbose:
                    print(f"  setting cid {external_cid} via CC ID {pci} to val {pcv}")
                self.change_setting(midi_channel, pci, pcv, verbose=False, get_response=False)
        last_setting = setting

    def change_setting_helper(self, channel, param_control_id, param_control_value, verbose=False, get_response=False):
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

    # Send a program change message
    # This is useful when changing the preset in a device
    # like the Fractal unit, to automate changes across presets
    def change_preset(self, channel, program):
        m = mido.Message(type="program_change", 
                         channel=channel, 
                         program=program)     
        self.outport.send(m)


if __name__ == '__main__':
    import sys
    m = MIDIController()
    m.change_preset(channel=0, program=int(sys.argv[1]))


