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


data, header = pyxdf.load_xdf('ClosedEyes.xdf')
availableSignals = ['Plux - PZT', 'Plux - EDA', 'Plux - TMP', 'Plux - EMG', 'Plux - ECG',
                    'Plux - EEG','Plux - ACC','EEG']

alldataAvailabe = pd.DataFrame()
pluxdp = pd.DataFrame()
viveEEGpd = pd.DataFrame()
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



#get names of collums
dataNames = alldataAvailabe.columns.values
channelQuant = dataNames.size-1

if channelQuant % numOfCombineGraphs == 0:
    numofLines = math.floor(channelQuant / numOfCombineGraphs)
else:
    numofLines = math.floor(channelQuant / numOfCombineGraphs)+1



## PLOTS
figure, axes = plt.subplots(numofLines,numOfCombineGraphs, sharex=True, figsize=(25,12))
figure.suptitle('Biosignals')

sns.lineplot('Timestamp', 'value', hue='variable',data=pd.melt(alldataAvailabe, 'Timestamp'),ax= axes[0,0])
sns.lineplot('Timestamp', 'value', hue='variable',data=pd.melt(pluxdp, 'Timestamp'),ax= axes[0,1])
sns.lineplot('Timestamp', 'value', hue='variable',data=pd.melt(viveEEGpd, 'Timestamp'),ax= axes[0,2])


rowCount = 1
lineCount = 0
for channel in range(dataNames.size):
    if dataNames[channel] != 'Timestamp':
        if rowCount<numofLines:
            if lineCount<numOfCombineGraphs:
                sns.lineplot(ax=axes[rowCount, lineCount], data=alldataAvailabe, x='Timestamp', y=dataNames[channel])
                print ("["+str(rowCount)+"],["+str(lineCount)+"] - "+dataNames[channel])
                lineCount += 1
            else:
                lineCount = 0
                rowCount += 1





#sns.lineplot(ax=axes[1,0], data = alldataAvailabe, x= 'Timestamp', y ='Plux - PZT')
#sns.lineplot(ax=axes[0,3], data = pluxpd, x= 'Timestamp', y ='plux1')
#sns.lineplot(ax=axes[1,0], data = pluxpd, x= 'Timestamp', y ='plux2')
#if 'plux3' in df_merge:
    #sns.lineplot(ax=axes[0,4], data=pluxpd, x='Timestamp', y='plux3')

#sns.lineplot('Timestamp', 'value', hue='variable',data=pd.melt(eegpd, 'Timestamp'),ax= axes[2,3])
#sns.lineplot(ax=axes[1,1], data = df_merge, x= 'Timestamp', y ='AF3')
#sns.lineplot(ax=axes[1,2], data = df_merge, x= 'Timestamp', y ='AF4')
#sns.lineplot(ax=axes[1,3], data = df_merge, x= 'Timestamp', y ='Fp1')
#sns.lineplot(ax=axes[2,0], data = df_merge, x= 'Timestamp', y ='Fp2')
#sns.lineplot(ax=axes[2,1], data = df_merge, x= 'Timestamp', y ='AF7')
#sns.lineplot(ax=axes[2,2], data = df_merge, x= 'Timestamp', y ='AF8')



plt.show()
