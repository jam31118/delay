"""Utility for finding zeros"""

from scipy.optimize import bisect

def find_all_zeros(fx, x_array):
    f_array = fx(x_array)
    zero_transition_indices, = np.nonzero(np.convolve(f_array > 0, [-1,1], 'valid'))
    assert zero_transition_indices[-1] < len(x_array) - 1
    x_at_zeros = []
    for idx in zero_transition_indices:
        try: x_at_zero = bisect(fx, x[idx], x[idx+1])
        except ValueError as e:
            print("a: {} / b: {} / f(a): {} / f(b): {}".format(x[idx], x[idx+1], fx(x[idx]), fx(x[idx+1])))
            raise e
        x_at_zeros.append(x_at_zero)
    return x_at_zeros

