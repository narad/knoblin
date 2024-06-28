from typing import Dict, List
import yaml
from pathlib import Path
from random import sample


class SweepInfo:

    def __init__(self, comment, params, controls=None):
        self.comment = comment
        self.params = params
        self.controls = controls


class ParamSweep:

    def __init__(self, names, min_val, max_val, step):
        self.names = names
        self.min_val = min_val
        self.max_val = max_val
        self.step = step


class Sweeper:

    def __init__(self, config, max_samples, verbose=True):
        self.config = config        
        self.sweeps = [(sw.comment, list(self.sweep_helper(sw.params))) for sw in config.infos]
        for i in range(0, len(self.sweeps)):
            sweep_name, sweep = self.sweeps[i]
            if max_samples > -1 and len(sweep) > max_samples:
                if verbose:
                    print(f"Reducing the number of sweeps in {sweep_name},\n  {len(sweep)} -> {max_samples}")
                sweep = sample(sweep, max_samples)
                self.sweeps[i] = sweep_name, sweep



    def sweep_helper(self, param_list: List[ParamSweep]):
        if len(param_list) > 1:
            first, rest = param_list[0], param_list[1:]
            settings = self.sweep_helper(rest) #, tied_params)
        else:
            first = param_list[0]
            settings = [{}]

        for setting in settings:
            mult = 100
            for v in range(int(first.min_val * mult), int(first.max_val * mult) + 1, int(first.step * mult)):
                v = v / mult
                z = {**setting, **{pname : v for pname in first.names}}
                yield z


    def write(self, out_file: Path, di_file: Path):
        # print(out_file)
        # Path(out_file).parents[0].mkdir(parents=True, exist_ok=True)
        with open(out_file, "w") as settings_file:
            settings_file.write(f"brand: {self.config.brand_name}\n")
#            settings_file.write(f"vst_name: {self.config.vst_name}\n")
            settings_file.write(f"device: {self.config.device_name}\n")                    
            settings_file.write(f"device_type: {self.config.device_type}\n")                    
            settings_file.write(f"data_type: {self.config.data_type}\n")                    
            settings_file.write(f"di_file: {di_file.name}\n")
            settings_file.write("files:\n")
            i = 0
            for sweep_name, sweep in self.sweeps:
                for setting in sweep:
                    settings_file.write(f"  - filename: {i:08d}.wav\n" +
                                        "    settings:\n")
                    for param_name, param_val in setting.items():
                        settings_file.write(f"    - \"{param_name}\": {param_val}\n")
                    i += 1
            settings_file.write("defaults:\n")
            for param_name, param_val in self.config.default_values().items():
                settings_file.write(f"    - \"{param_name}\": {param_val}\n")
                
                # settings_file.write(f"  - name: \"{param_name}\"\n")
                # settings_file.write(f"    value: {param_val}\n")



class SweepConfig:

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
        if 'model' in info:
            self.model = info['model']
        if 'preset_id' in info:
            self.preset_id = info['preset_id']
        if 'defaults' not in info:
            self.default_value_dict = {}
        else:
            self.default_value_dict = { p['name']: p['value'] for p in info['defaults']}
        if 'controls' in info:
            control_mapping = {}
            for tup in info['controls']:
                control_mapping[tup['name']] = tup['value']
            self.control_mapping = control_mapping

        # if 'controls' in info:
        #     self.midi_channel = info['controls']['midi_channel']
        #     midi_ccs = {}
        #     for p in info['controls']['midi_mapping']:
        #         midi_ccs[p['name']] = p['midi']
        #     self.midi_mapping = midi_ccs
        self.infos = [self.parse_sweep(sd) for sd in info['sweeps']]


    def parse_sweep(self, sweep_dict):
        params = [ParamSweep(p['name'], p['min'], p['max'], p['step']) for p in sweep_dict['params']]
        return SweepInfo(comment=sweep_dict['comment'], 
                         params=params)


    def flatten(self, l):
        return [x for row in l for x in l]


    def tunable_parameters(self) -> List[str]:
        return self.flatten(self.sweeps[0].params)

    def sweeps(self):
        return self.sweeps


    def default_values(self) -> Dict[str, float]:
        return self.default_value_dict







    # @staticmethod
    # def load()



# old code from when sweeps had to stay as generators
# #from itertools import chain

# def chain(*iterables): 
#   for iterable in iterables: yield from iterable 
