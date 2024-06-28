"""
The main data generation script

"""
import sys
import argparse
from pathlib import Path
import shutil
from typing import Dict, List
import time
from tqdm import tqdm
import numpy as np

import sounddevice as sd
import soundfile as sf

from knoblin.sweeps import Sweeper, SweepConfig
from knoblin.hardware import HardwareConfig
from knoblin.midi.midi_controller import MIDIController

# audio notification
from pydub import AudioSegment
from pydub.playback import play

controller = MIDIController()


def generate_data(di_file, output_dir, device_config, sweep_config, args):

    midi_channel = device_config.midi_channel
    # External control ID -> MIDI CC
    midi_mapping = device_config.midi_mapping
    # Control name str -> External control ID
    control_mapping = sweep_config.control_mapping
    print(sweep_config.control_mapping)
#    print(preset_mapping)

    # Load DI
    di, sr = sf.read(di_file, dtype='float32', samplerate=None)
    assert len(di.shape) == 1, f"Only mono audio is supported (DI shape = {di.shape})"

    # Print sample rate
    if args.verbose:
        print("Sample rate of DI track: ", sr)

    # Add padding
    di = np.concatenate([di, np.zeros([args.pad_samples])])

    # Compute sweeps
    sweeper = Sweeper(sweep_config, max_samples=args.max_samples)
    file_offset = 0
    for sweep_name, sweep in sweeper.sweeps:
        sweep = list(sweep)
        num_settings = len(sweep)

        print(f"Performing sweep \"{sweep_name}\"")
        last_setting = None
        for setting in tqdm(sweep):
            if args.verbose:
                print(setting)       
            # Set settings on device
            # for pnam, pci in control_mapping.items():
            for pname, pval in setting.items():
                if last_setting is not None and setting[pname] == last_setting[pname]:
                    continue
                else:
                    if args.verbose:
                        print(pname, "\t", pval)
                    external_cid = control_mapping[pname]
                    pci =  midi_mapping[external_cid]
                    pcv = knob2midi(int(pval * 10))
                    if args.verbose:
                        print(f"  setting cid {external_cid} via CC ID {pci} to val {pcv}")
                    controller.change_setting(midi_channel, pci, pcv, verbose=False, get_response=False)
            last_setting = setting

            # Recording
            if args.verbose:
                print("recording")
            recording = sd.playrec(di, sr, device=0, channels=args.recording_channel)
            status = sd.wait()
            recording = recording[:,args.recording_channel-1]

            # Write recording to file
            pstring = '_'.join([f"{k}-{v}" for k,v in setting.items()])
            sf.write(output_dir / f"{file_offset:08d}.wav", recording, sr)

            # Update offset to new total number of files in directory
            file_offset += 1

    # write out settings in index file
    sweeper.write(output_dir / "settings.yaml", di_file)

    # possibly copy the DI to the output directory
    if args.copy_di:
        shutil.copy(di_file, output_dir / di_file.name)


def knob2midi(knob_value):
    return int((127 / 10) * knob_value)


def generate_data_from_fractal(settings, controller, pci, pcv, sleep_time=1, last_settings=None):
    # for param_name, param_val in settings.items():
    #     print(param_name, param_val)
    for pnam, pci in control_mapping.items():
        pcv = knob2midi(10)
        controller.change_setting(0, pci, pcv, True)
        time.sleep(sleep_time)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Options for VST rendering.')
    parser.add_argument('--di_file', type=str, required=True,
                        help='path to a DI wav file, as str.  can provide multiple files separated by comma')
    parser.add_argument('--sweep_conf_file', type=Path, required=True,
                        help='path to a sweep config file.  If a directory, will iterate over all conf files contained within')
    parser.add_argument('--device_conf_file', type=Path, required=True,
                        help='path to a hardware config file')
    parser.add_argument('--output_dir', type=Path, required=True,
                        help="the (root) directory where data will be written")
    parser.add_argument('--verbose', type=bool, default=False,
                        help="whether to print logging information")
    parser.add_argument('--max_samples', type=int, default=-1,
                        help="max number of samples.  If less than total specified sweeps, sample uniformly.")
    parser.add_argument('--copy_di', type=bool, default=True, 
                        help="copy the DI file to the output_dir for future reference")
    parser.add_argument('--play_alarm', type=bool, default=False,
                        help="play an alarm sound when finished")
    parser.add_argument('--recording_channel', type=int, default=1,
                        help="the channel ID on the interface for the recording input")
    parser.add_argument('--pad_samples', type=int, default=22050,
                        help="the amount of blank padding to add to the end of the DI.  Not having padding may mean some audio is cut due to latency.")
    parser.add_argument('--set_preset', type=bool, default=False,
                        help="send a program change MIDI command to the device prior to sweep (otherwise assume device is setup \
                              for current config file).  Necessary for batch processing of multiple device sweep configs.")
    args = parser.parse_args()

    # Setup hardware config
    device_config = HardwareConfig(args.device_conf_file)

    # Read config files
    if args.sweep_conf_file.is_file():
        sweep_configs = [SweepConfig(args.sweep_conf_file)]
    elif args.sweep_conf_file.is_dir():
        print("loading...")
        sweep_configs = [SweepConfig(f) for f in args.sweep_conf_file.glob("*.yaml")]
    sweep_configs.sort(key=lambda x: x.model)

    # Collect possibly multiple DI files
    di_files = [Path(f) for f in args.di_file.split(',')]

    print(len(sweep_configs))
    # Loop through all conf files
    for sweep_config in sweep_configs:
        if args.set_preset:
            print(sweep_config.model)
#            print(device_config.preset_mapping)
#            print(sweep_config.model in device_config.preset_mapping.keys())
#            preset_id = device_config.preset_mapping[sweep_config.model]

            print(f"Model {sweep_config.model} is setup on preset {sweep_config.preset_id}")
            controller.change_preset(channel=device_config.midi_channel, program=sweep_config.preset_id)
            time.sleep(1)

        # Loop through all given DI
        root_output_dir = args.output_dir
        for di_file in di_files:
            output_dir = root_output_dir / device_config.brand_name / device_config.device_name / sweep_config.model / args.sweep_conf_file.stem / di_file.stem
            print(str(output_dir))
            output_dir.mkdir(parents=True, exist_ok=True)

            # Set rendering args for this specific run
            # args.__dict__['di_file'] = di_file
            # args.__dict__['output_dir'] = output_dir
            if args.verbose:
                print(args)
            generate_data(di_file, output_dir, device_config, sweep_config, args)

    if args.play_alarm:
        alarm = AudioSegment.from_mp3('sounds/completion_notification.wav')
        play(alarm)
        play(alarm)









#    di = data[start_second * sr:(start_second + duration) * sr]

# Probably deprecated holdovers from tone-render
#     parser.add_argument('--logging', type=str, choices=['stdout', 'console', 'both'], default='stdout',
#                         help="destination of logging messages (default is 'stdout', but can also print to REAPER 'console'.")


#     # Set the logging mode
#     global MSG_MODE
#     MSG_MODE = args.logging


# def msg(message: str) -> None:
#     """
#     Outputs the logging message to stdout or to the REAPER console
#     Args:
#         message (str): The logging message
#     Returns:
#         None
#     """
#     if MSG_MODE in ('stdout', 'both'):
#         print(message)
#     if MSG_MODE in ('console', 'both'):
#         RPR.ShowConsoleMsg(message + "\n")

