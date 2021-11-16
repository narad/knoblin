

class DeviceSettingsSweep:

    def __init__(self, control_dict):
        self.control_dict = control_dict
        self.sweep_dict = self.full_sweep()

    def full_sweep(self, discretize_interval=1):
        sweep_dict = dict()
        for param in self.control_dict:
#             if param.parameter_type == "continuous":
#                 sweep_dict[param.name] = list(range(param.min_value, param.max_value, discretize_interval))
            if param.parameter_type == "discrete":
                sweep_dict[param.name] = [v.midi for v in param.settings]
        return sweep_dict


    def get_settings(self, sweep_dict=None):
        if sweep_dict is None:
            sweep_dict = self.sweep_dict
        k = list(sweep_dict.keys())[0]
        if len(sweep_dict) == 1:
            return [{k:v} for v in sweep_dict[k]]
        else:
            dict_copy = dict(sweep_dict)
            dict_copy.pop(k)
            inner_settings = self.get_settings(dict_copy)
            settings = []
            for v in sweep_dict[k]:
                for setting in inner_settings:
                    setting_copy = dict(setting)
                    setting_copy[k] = v
                    settings.append(setting_copy)
            return settings



#   def default_sweep(self):
#      {
# #             'volume': [2],
# #             'treble': [4, 8],
# #             'mids': [2, 5, 8],
# #             'freq': [3, 5, 7],
# #             'bass': [3],
# #             'gain': [3,6,9],
# #             'mid_type': [1, 2, 3],
# #             'q': [1, 2, 3],
# #             'diode': [1, 2, 3],
# #             'fuzz': [1, 2, 3]
# #         }