from os.path import abspath, join, dirname
import logging
import pyxdf
import sys
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

data, header = pyxdf.load_xdf('TestMeh.xdf')

for stream in data:

    print(stream['info']['name'][0])
    if stream['info']['name'][0] == 'Plux':
        print("There is a plux stream")

        #y = stream['time_series']
        #timeStamps = stream['time_stamps']
        #sns.lineplot(data=y)
        #if isinstance(y, list):
            # list of strings, draw one vertical line for each marker
            #for timestamp, marker in zip(stream['time_stamps'], y):
                #plt.axvline(x=timestamp)
                #print(f'Marker "{marker[0]}" @ {timestamp:.2f}s')
        #elif isinstance(y, np.ndarray):
            # numeric data, draw as lines
            #plt.plot(stream['time_stamps'], y)
        #else:
            #raise RuntimeError('Unknown stream format')

    if stream['info']['name'][0] == 'EEG':
        print("There is a EEG stream")

        y = stream['time_series']

        sns.lineplot(data= y )
        #for signal in y:
            #for value in signal:
                #sns.lineplot(value,stream['time_stamps'])






plt.show()