import numpy as np

ch_rej = np.asarray([1, 0, 0.5, 0, 0, 0, 0, 0, 1, 0]).mean()

ch_ent = np.asarray([1, 1, 0.5, 0, 0, 0, 0, 0, 1, 0]).mean()

ch_exit = np.asarray([1, 1, 0, 0.5, 1, 0.5, 0.5, 1, 0, 0.5]).mean()

or_rej = np.asarray([1, 1, 0, 0.5, 0, 0, 0, 0, 0, 1, 0]).mean()

or_ent = np.asarray([1, 1, 1, 0.5, 0, 0, 0, 0, 0, 1, 0]).mean()

or_exit = np.asarray([1, 1, 1, 0, 0.5, 1, 0.5, 0.5, 1, 0, 0.5]).mean()

print(ch_rej, ch_ent, ch_exit)
print(or_rej, or_ent, or_exit)
