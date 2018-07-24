"""Spectrogram Object"""

from os.path import isfile

import numpy as np

from .default import default_config, get_delay_value_array

class Spectrogram(object):

    def __init__(self, raw_file_path, num_of_delays, num_of_omega, delay_value_array):
        self.file_path = None
        if isfile(raw_file_path):
            self.file_path = raw_file_path
        else: raise IOError("Could not find raw file: {}".format(raw_file_path))
        assert self.file_path is not None

        assert int(num_of_delays) == num_of_delays
        self.num_of_delays = int(num_of_delays)
        assert int(num_of_omega) == num_of_omega
        self.num_of_omega = int(num_of_omega)
        assert len(delay_value_array) == int(num_of_delays)
        self.delay_value_array = delay_value_array

        self.data = self.load(self.file_path, self.num_of_delays, self.num_of_omega, self.delay_value_array)
        self.omega_array = self._get_omega_array(self.data)

    def _get_omega_array(self, data_array_3d):
        omega_array = data_array_3d[0,:,0]
        return omega_array

    def load(self, raw_file_path, num_of_delays, num_of_omega, delay_value_array):

        raw_data_array = np.loadtxt(raw_file_path)
        self._check_loaded_data(raw_data_array, num_of_omega, num_of_delays, delay_value_array)

        actual_num_of_rows, actual_num_of_columns = raw_data_array.shape
        new_shape = (num_of_delays, num_of_omega, actual_num_of_columns)
        data_array_3d = raw_data_array.reshape(new_shape)

        ## Check whether the reshaping was done in a proper and desired way
        assert np.all(raw_data_array[:num_of_omega, :] == data_array_3d[0])

        omega_array = data_array_3d[0,:,0]
        assert omega_array.shape == (num_of_omega,)

        return data_array_3d

    def _check_loaded_data(self, loaded_data_array, num_of_omega, num_of_delays, delay_value_array):

        num_of_dimension_of_raw_data_array = default_config["num_of_dimension_of_raw_data_array"]
        assert loaded_data_array.ndim == num_of_dimension_of_raw_data_array

        actual_num_of_rows, actual_num_of_columns = loaded_data_array.shape

        expected_num_of_rows = num_of_delays * num_of_omega
        expected_num_of_columns = default_config["expected_num_of_columns"]
        assert actual_num_of_rows == expected_num_of_rows
        assert actual_num_of_columns == expected_num_of_columns

    def __getitem__(self, index_exp):
        return self.data[index_exp]


    @classmethod
    def from_file(cls, raw_file_path, num_of_delays=None, num_of_omega=None, delay_value_array=None):
        assert isfile(raw_file_path)
        if num_of_delays is None: num_of_delays = default_config["num_of_delay_points"]
        if num_of_omega is None: num_of_omega = default_config["num_of_omega"]
        if delay_value_array is None: delay_value_array = get_delay_value_array()
        return cls(raw_file_path, num_of_delays, num_of_omega, delay_value_array)


