from os.path import abspath, join, dirname
import logging

import pandas as pd
import pyxdf
import sys
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import math


data, header = pyxdf.load_xdf('Markers.xdf')
availableSignals = ['Plux - PZT', 'Plux - EDA', 'Plux - TMP', 'Plux - EMG', 'Plux - ECG',
                    'Plux - EEG','Plux - ACC','EEG','MarkerStream']

alldataAvailabe = pd.DataFrame()
pluxdp = pd.DataFrame()
viveEEGpd = pd.DataFrame()
markerspd = pd.DataFrame()
numOfCombineGraphs = 3


def column(matrix, i):
    return [row[i] for row in matrix]

def SearchStream (name):

    newpd = pd.DataFrame()
    if name == 'Plux - PZT' or name =='Plux - EDA' or name == 'Plux - TMP' or name == 'Plux - EMG' or name == 'Plux - ECG' or name == 'Plux - EEG' or name == 'Plux - ACC':
        for stream in data:
            if stream['info']['name'][0] == name:
                print("There is a " + name + " stream")
                numOfChannels =int(stream['info']['channel_count'][0])
                print (numOfChannels)
                y = stream['time_series']
                timeStamps = stream['time_stamps']
                newpd = pd.DataFrame([timeStamps], index=['Timestamp']).T
                for channel in range(numOfChannels):
                    yline = column(y, channel)
                    newpd[""+name+""] = yline



    elif name == 'EEG':
        for stream in data:
            if stream['info']['name'][0] == 'EEG':
                print("There is a EEG stream")

                eegy = stream['time_series']
                timeStamps = stream['time_stamps']
                eegy1 = column(eegy, 0)
                eegy2 = column(eegy, 1)
                eegy3 = column(eegy, 2)
                eegy4 = column(eegy, 3)
                eegy5 = column(eegy, 4)
                eegy6 = column(eegy, 5)
                newpd = pd.DataFrame([timeStamps, eegy1, eegy2, eegy3, eegy4, eegy5, eegy6],
                                     index=['Timestamp', 'AF3', 'AF4', 'Fp1', 'Fp2', 'AF7', 'AF8']).T

    elif name == 'MarkerStream':
        for stream in data:
            if stream['info']['name'][0] == name:
                print("There is a " + name + " stream")
                eventnames = stream['time_series']
                timeStamps = stream['time_stamps']
                yline = column(eventnames, 0)

                midpd = pd.DataFrame([timeStamps],
                                     index=['Timestamp']).T
                newstringpd = pd.Series([yline],name="Events").T
                newpd = pd.concat([midpd,newstringpd],axis = 1)

    if not newpd.empty:
        return newpd
    else:
        print("There wasnt a "+ name + " stream")


for names in availableSignals:
    print("is there a " + names + "?")
    addpd = SearchStream(names)
    if addpd is not None:
        alldataAvailabe= alldataAvailabe.append(addpd)
    if "Plux" in names:
        pluxdp =pluxdp.append(addpd)
    elif names == "EEG":
        viveEEGpd = viveEEGpd.append(addpd)
    elif names == "MarkerStream":
        markerspd = markerspd.append(addpd)


#get names of collums
dataNames = alldataAvailabe.columns.values
channelQuant = dataNames.size-1

print(channelQuant)
if channelQuant % numOfCombineGraphs == 0:
    numofLines = math.floor(channelQuant / numOfCombineGraphs)
else:
    numofLines = math.floor(channelQuant / numOfCombineGraphs)+2

print(numofLines)

## PLOTS
figure, axes = plt.subplots(numofLines,numOfCombineGraphs, sharex=True, figsize=(25,12))
figure.suptitle('Biosignals')

sns.lineplot('Timestamp', 'value', hue='variable',data=pd.melt(alldataAvailabe, 'Timestamp'),ax= axes[0,0])
sns.lineplot('Timestamp', 'value', hue='variable',data=pd.melt(pluxdp, 'Timestamp'),ax= axes[0,1])
sns.lineplot('Timestamp', 'value', hue='variable',data=pd.melt(viveEEGpd, 'Timestamp'),ax= axes[0,2])


rowCount = 1
lineCount = 0
for channel in range(dataNames.size):
    if dataNames[channel] != 'Timestamp' :
        print("graph for "+dataNames[channel])
        if rowCount<numofLines:
            if lineCount<numOfCombineGraphs:
                sns.lineplot(ax=axes[rowCount, lineCount], data=alldataAvailabe, x='Timestamp', y=dataNames[channel])
                print ("["+str(rowCount)+"],["+str(lineCount)+"] - "+dataNames[channel])
                lineCount += 1
            else:
                rowCount += 1
                lineCount = 0
                sns.lineplot(ax=axes[rowCount, lineCount], data=alldataAvailabe, x='Timestamp', y=dataNames[channel])
                print("[" + str(rowCount) + "],[" + str(lineCount) + "] - " + dataNames[channel])
                lineCount += 1



plt.show()
