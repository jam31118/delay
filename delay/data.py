"""Utilitiy for data file Input/Output"""

from os.path import basename, isfile, splitext, join, dirname, isdir
from os import listdir, mkdir

from numpy import loadtxt
from pandas import read_csv


def read_peak_data(peaks_file_path):
    "Support one of the following file formats: '.txt', '.csv'"
    file_extension = splitext(peaks_file_path)[-1]
    raw_peaks_array = None
    if file_extension == ".txt":
        raw_peaks_array = loadtxt(peaks_file_path)
    elif file_extension == ".csv":
        raw_peaks_array = read_csv(peaks_file_path, header=None).values
    else: raise ValueError("Unexpected file extension for peaks_file_path: {}".format(peaks_file_path))
    assert raw_peaks_array is not None
    return raw_peaks_array


