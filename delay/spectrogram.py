"""Spectrogram Object"""

from os.path import isfile

import numpy as np
from scipy.signal import find_peaks
from vis.plot import construct_catesian_mesh_for_pcolormesh
from matplotlib.axes import Axes

from .default import default_config, get_delay_value_array, get_find_peaks_kwargs
from .fzero import find_all_zeros


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

    def find_peak_from_single_spectrum(self, delay_index, num_of_explicit_peaks, num_of_poly=10, find_peaks_kwargs=None):
        data_array_3d = self.data

        omega_array = data_array_3d[delay_index,:,0]
        partial_spectrum_1 = data_array_3d[delay_index,:,1]
        partial_spectrum_2 = data_array_3d[delay_index,:,2]
        total_spectrum = data_array_3d[delay_index,:,3]
        
        if find_peaks_kwargs is None:
            find_peaks_kwargs = get_find_peaks_kwargs()
        peaks_indice, _ = find_peaks(total_spectrum, **find_peaks_kwargs)

        if len(peaks_indice) > num_of_explicit_peaks: peaks_indice = peaks_indice[-num_of_explicit_peaks:]

        omega_at_peaks = self.omega_array[peaks_indice]
        #estimated_peak_interval = peaks_indice[-1] - peaks_indice[-2]
        assert len(omega_at_peaks) >= 2
        estimated_omega_interval = omega_at_peaks[-1] - omega_at_peaks[-2]
       

#        omega_range_min = omega_at_peaks[0] - estimated_omega_interval // 3
        omega_range_min = omega_at_peaks[-1] - (num_of_explicit_peaks - 1) * estimated_omega_interval - estimated_omega_interval // 3
        omega_range_max = omega_at_peaks[-1] + estimated_omega_interval // 3
        
        sliced_omega_array_mask = (self.omega_array < omega_range_max) & (self.omega_array > omega_range_min)
        sliced_omega_array = self.omega_array[sliced_omega_array_mask]
        sliced_total_spec = total_spectrum[sliced_omega_array_mask]

        num_of_omega_in_slice = len(sliced_omega_array)

        polyfit_results = np.polyfit(sliced_omega_array, sliced_total_spec, num_of_poly)
        fitted_poly = np.poly1d(polyfit_results)

        omega_at_peaks_by_fitting = find_all_zeros(fitted_poly.deriv(m=1), sliced_omega_array, target='maximum')
        num_of_found_peaks_from_fitting = omega_at_peaks_by_fitting.size

        omega_at_peaks_to_return = np.empty(num_of_explicit_peaks, dtype=float)
        if num_of_found_peaks_from_fitting == num_of_explicit_peaks:
            omega_at_peaks_to_return[:] = omega_at_peaks_by_fitting
        elif num_of_found_peaks_from_fitting < num_of_explicit_peaks:
            omega_at_peaks_to_return[-num_of_found_peaks_from_fitting:] = omega_at_peaks_by_fitting
            num_of_nan_in_result = num_of_explicit_peaks - num_of_found_peaks_from_fitting
            omega_at_peaks_to_return[:num_of_nan_in_result] = np.nan
        elif num_of_found_peaks_from_fitting > num_of_explicit_peaks:
#            raise ValueError("The `num_of_explicit_peaks` is too small: {}".format(num_of_explicit_peaks))
            omega_at_peaks_to_return[:] = omega_at_peaks_by_fitting[-num_of_explicit_peaks:]
        else: raise Exception("Unexpected Exception")

        return omega_at_peaks_to_return

    def find_peaks_for_all_delay(self, num_of_explicit_peaks, **single_peak_find_kwargs):
        out_array_shape = (self.num_of_delays, num_of_explicit_peaks+1)
        out_array = np.empty(out_array_shape, dtype=float)
        out_array[:,0] = self.delay_value_array
        for delay_index in range(self.num_of_delays):
            out_array[delay_index,1:] = self.find_peak_from_single_spectrum(delay_index, num_of_explicit_peaks, **single_peak_find_kwargs)
        return out_array

    def draw_spectrogram_on_axes(self, ax, **pcolormesh_kwargs):
        assert isinstance(ax, Axes)
        X, Y = construct_catesian_mesh_for_pcolormesh(self.delay_value_array, self.omega_array)
        total_spectrum_column_index_in_data = 3
        data_array_2d = self.data[:,:,total_spectrum_column_index_in_data]
        pcm = ax.pcolormesh(X, Y, data_array_2d, **pcolormesh_kwargs)
        return pcm


