import yaml

class HardwareConfig:

    def __init__(self, filename) -> None:
        self.read(filename)


    def read(self, filename, verbose=False) -> None:
        with open(filename) as infile:
            info = yaml.safe_load(infile)
        self.brand_name = info['brand']
        try:
            self.vst_name = info['vst']
        except:
            pass
        self.device_name = info['device']
        self.device_type = info['device_type']
        self.data_type = info['data_type']
        if 'controls' in info:
            try:
                self.midi_channel = info['controls']['midi_channel']
                midi_ccs = {}
                for p in info['controls']['midi_mapping']:
                    midi_ccs[p['external_id']] = p['midi']            
                # for p in info['controls']['midi_mapping']:
                #     midi_ccs[p['name']] = p['midi']
                self.midi_mapping = midi_ccs
            except:
                print("Maybe not a MIDI based config file?")

            try:
                name2servo = {}
                for c in info['controls']:
                    name2servo[c['name']] = c['value']
                self.control_mapping = name2servo
            except:
                print("error adding servo controls")

        if 'preset_mapping' in info:
            self.preset_mapping = {}
            for p in info['preset_mapping']:
                self.preset_mapping[p['name']] = p['preset']