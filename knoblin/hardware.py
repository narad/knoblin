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
            self.midi_channel = info['controls']['midi_channel']
            midi_ccs = {}
            for p in info['controls']['midi_mapping']:
                midi_ccs[p['external_id']] = p['midi']            
            # for p in info['controls']['midi_mapping']:
            #     midi_ccs[p['name']] = p['midi']
            self.midi_mapping = midi_ccs

        if 'preset_mapping' in info:
            self.preset_mapping = {}
            for p in info['preset_mapping']:
                self.preset_mapping[p['name']] = p['preset']