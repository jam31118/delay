"""Utility for finding zeros"""

from scipy.optimize import bisect
import numpy as np

def find_all_zeros(fx, x_array, target='both'):
    f_array = fx(x_array)
    convolved = np.convolve(f_array > 0, [-1,1], 'valid')
    zero_transition_indices, = np.nonzero(convolved)
    target_zero_transition_indices = None
    if target == 'maximum':
        target_zero_transition_indices, = np.nonzero(convolved > 0)
#        target_zero_transition_indices = convolved[convolved[zero_transition_indices] > 0]
    elif target == 'minimum':
        target_zero_transition_indices, = np.nonzero(convolved < 0)
#        target_zero_transition_indices = convolved[convolved[zero_transition_indices] < 0]
    elif target == 'both':
        target_zero_transition_indices = zero_transition_indices
    else: raise ValueError("Unexpected value for argument `target`")
    assert target_zero_transition_indices is not None

#    zero_transition_indices = None
#    if target == 'maximum':
#        zero_transition_indices =  
#    zero_transition_indices, = np.nonzero()

    assert zero_transition_indices[-1] < len(x_array) - 1
#    target_zero_transition_indices = None
#    if target == 'maximum':
#        target_zero_transition_indices = zero_transition_indices[zero_transition_indices > 0]
#    assert target_zero_transition_indices is not None
    x = x_array  # aliasing
    x_at_zeros = []
    for idx in target_zero_transition_indices:
#    for idx in zero_transition_indices:
        try: x_at_zero = bisect(fx, x[idx], x[idx+1])
        except ValueError as e:
            print("a: {} / b: {} / f(a): {} / f(b): {}".format(x[idx], x[idx+1], fx(x[idx]), fx(x[idx+1])))
            raise e
        x_at_zeros.append(x_at_zero)
    return np.array(x_at_zeros)

