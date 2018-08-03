from os.path import isfile
import re


def extract_substring_from_filename(filename, regex):
    assert isfile(filename)
    search_obj = re.search(regex, filename)
    assert (search_obj is not None) and (len(search_obj.groups()) == 1)
    V_str, = search_obj.groups()
    return V_str

def fill_string_and_return_scalar(string, full_str_len, num_of_order_below_punc):
    num_of_order_to_raise = full_str_len - len(string)
    assert num_of_order_to_raise >= 0
    return int(string) * pow(10, num_of_order_to_raise - num_of_order_below_punc)


def extract_V_str_from_filename(filename):
    return extract_substring_from_filename(filename, ".*V([0-9]+).*")

def V_str_to_V_float(V_str):
    return fill_string_and_return_scalar(V_str, full_str_len = 4, num_of_order_below_punc = 3)

def extract_V_float_from_filename(filename):
    return V_str_to_V_float(extract_V_str_from_filename(filename))


def extract_w_str_from_filename(filename):
    return extract_substring_from_filename(filename, ".*w([0-9]+).*")

def w_str_to_w_float(w_str):
    return fill_string_and_return_scalar(w_str, full_str_len = 4, num_of_order_below_punc = 3)

def extract_w_float_from_filename(filename):
    return w_str_to_w_float(extract_w_str_from_filename(filename))


