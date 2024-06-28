import sounddevice as sd
import soundfile as sf
import time
import IPython
import time
from collections import deque

# Serialization for device config files
from munch import munchify
import yaml

# Package imports
from midis.midi_controller import MIDIController


class Recorder:

	def __init__(self):
		self.setup_device()


	def setup_device(self):
		# Setup Audio Recording loop
		device_info = sd.query_devices(0, 'input')
		print(device_info)

		samplerate = int(device_info['default_samplerate'])

		sd.default.samplerate = samplerate
		sd.default.channels = 2
		print(device_info)


	def record(self, audio_data, sr, filename=None):
		# Recording
		recording = sd.playrec(audio_data, sr, device=0, channels=1)
		status = sd.wait()

		if filename is not None:
			sf.write(filename, recording, sr)
		return recording





# # Input name of device
# device_name = "Boss SD-1w"

# # Select the type of controller
# controller_type = ["MIDI", "arduino"][0]

# midi_sleep_dur = 2
# # install mido / python-rtmidi
# #data_dir = "out/"
# data_dir = "./data/" #"/Volumes/16GB THUMBD/data/chase bliss mkII/"
# input_file = '/Users/narad/Desktop/projects/tone-render/di/real/lorcan/003_lorcan_metal_rhythm.wav' 
# #'/Users/narad/Desktop/projects/amp-space/data/scripts/python/test_di.wav'
# start_second = 3
# duration = 6

# if controller_type == "MIDI":
#     controller = MIDIController()
# else: # Arduino
#     controller = ServoController()





if __name__ == '__main__':
	rec = Recorder()






# # Read input file
# data, sr = sf.read(input_file, dtype='float32', samplerate=None)
# print("Sample rate of DI track: ", sr)
# data = data[start_second * sr:(start_second + duration) * sr]

# # Display to test
# sf.write(f"{data_dir}di.wav", data, sr)
# IPython.display.Audio(data, rate=sr)




