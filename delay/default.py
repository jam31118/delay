"""Default Configuration"""

import numpy as np

default_config = {
    "num_of_omega": 291,
    "num_of_delay_points": 81,
    "min_delay_value": -200,
    "delay_grid_interval": 5,
    "expected_num_of_columns": 4,
    "num_of_dimension_of_raw_data_array": 2,
    "expected_width_in_omega_space": 12.5,
    "prominence": 0.005
}

def get_delay_value_array(dtype=float):
    min_delay_value = default_config["min_delay_value"]
    num_of_delays = default_config["num_of_delay_points"]
    delay_grid_interval = default_config["delay_grid_interval"]
    delay_value_array = min_delay_value + np.arange(num_of_delays, dtype=dtype) * delay_grid_interval
    return delay_value_array

def get_find_peaks_kwargs(expected_width_in_omega_space=None, prominence=None):
    if expected_width_in_omega_space is None:
        expected_width_in_omega_space = default_config["expected_width_in_omega_space"]
    width = expected_width_in_omega_space / 4.0
    if prominence is None:
        prominence = default_config["prominence"]
    return {'width':width, 'prominence':prominence}
