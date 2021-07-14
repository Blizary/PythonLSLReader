from os.path import abspath, join, dirname
import logging
import pyxdf
import sys
import matplotlib.pyplot as plt
import numpy as np

logging.basicConfig(level=logging.DEBUG)  # Use logging.INFO to reduce output
if len(sys.argv) > 1:
    fname = sys.argv[1]
else:
    fname = abspath(join(dirname(__file__), '..', '..', 'Test.xdf'))
streams, fileheader = pyxdf.load_xdf(fname)

for stream in data:
    y = stream['time_series']

    if isinstance(y, list):
        # list of strings, draw one vertical line for each marker
        for timestamp, marker in zip(stream['time_stamps'], y):
            plt.axvline(x=timestamp)
            print(f'Marker "{marker[0]}" @ {timestamp:.2f}s')
    elif isinstance(y, np.ndarray):
        # numeric data, draw as lines
        plt.plot(stream['time_stamps'], y)
    else:
        raise RuntimeError('Unknown stream format')

plt.show()