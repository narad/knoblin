
from knoblin.midi.midi_controller import MIDIController, knob2midi
from knoblin.sweeps import ParamSweep, SweepInfo
import time

# The parameters and their MIDI CC mapping as set in the FM3
# (these are user-defined and must set before running the script)
control_mapping = {
    'Drive': 11,
    'Bass': 12,
    'Mid': 13,
    'Treble': 14,
}


def generate_data_from_fractal(args):
    controller = MIDIController()
    while True:
        for pnam,pci in control_mapping.items():
            pcv = knob2midi(10)
            controller.change_setting(0, pci, pcv, True)
            time.sleep(1)


def knob2midi(knob_value):
    return int((127 / 10) * knob_value)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Options for VST rendering.')
    parser.add_argument('--di_file', type=str, required=True,
                        help='path to a DI wav file, as str.  can provide multiple files separated by comma')
    parser.add_argument('--device_name', type=str, required=True,
                        help='name of the device (such as Soldano SLO 100)')
    parser.add_argument('--device_type', type=str, required=True,
                        help='type of the device (such as Pedal:chorus)')
    parser.add_argument('--output_dir', type=Path, required=True,
                        help="the (root) directory where data will be written")
    parser.add_argument('--verbose', type=bool, default=False,
                        help="whether to print logging information")
    parser.add_argument('--max_samples', type=int, default=-1,
                        help="max number of samples.  If less than total specified sweeps, sample uniformly.")
    parser.add_argument('--logging', type=str, choices=['stdout', 'console', 'both'], default='stdout',
                        help="destination of logging messages (default is 'stdout', but can also print to REAPER 'console'.")
    args = parser.parse_args()

	generate_data_from_fractal(args)