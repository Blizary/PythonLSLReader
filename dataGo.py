from os.path import abspath, join, dirname
import logging

import pandas as pd
import pyxdf
import sys
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

data, header = pyxdf.load_xdf('Plux3.xdf')

def column(matrix, i):
    return [row[i] for row in matrix]

def SearchStream (name):

    if name == 'Plux':
        for stream in data:
            print(stream['info']['name'][0])
            if stream['info']['name'][0] == 'Plux':
                print("There is a plux stream")
                numOfChannels =int(stream['info']['channel_count'][0])
                print (numOfChannels)
                y = stream['time_series']
                timeStamps = stream['time_stamps']
                newpd = pd.DataFrame([timeStamps], index=['Timestamp']).T
                for channel in range(numOfChannels):
                    #newpd['Type'] = "plux"+str(channel)
                    yline = column(y, channel)
                    newpd["plux"+str(channel)] = yline



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

    return newpd




pluxpd = SearchStream('Plux')
eegpd = SearchStream('EEG')

df_merge = pd.merge(pluxpd,eegpd,on='Timestamp',how='outer')

df = pd.DataFrame(data = np.random.randint(low=0,high=2,size=(10,5)),
                  columns=['Mon','Tues','Weds','Thurs','Fri'])

#figure, axes = plt.subplots(3, 4, sharex=True, figsize=(25,12))
#figure.suptitle('Biosignals')

#sns.lineplot('Timestamp', 'value', hue='variable',data=pd.melt(df_merge, 'Timestamp'),ax= axes[0,0])
#sns.lineplot('Timestamp', 'value', hue='variable',data=pd.melt(pluxpd, 'Timestamp'),ax= axes[0,1])
#sns.lineplot(ax=axes[0,2], data = pluxpd, x= 'Timestamp', y ='plux0')
#sns.lineplot(ax=axes[0,3], data = pluxpd, x= 'Timestamp', y ='plux1')
#sns.lineplot(ax=axes[1,0], data = pluxpd, x= 'Timestamp', y ='plux2')

#sns.lineplot('Timestamp', 'value', hue='variable',data=pd.melt(eegpd, 'Timestamp'),ax= axes[2,3])
#sns.lineplot(ax=axes[1,1], data = df_merge, x= 'Timestamp', y ='AF3')
#sns.lineplot(ax=axes[1,2], data = df_merge, x= 'Timestamp', y ='AF4')
#sns.lineplot(ax=axes[1,3], data = df_merge, x= 'Timestamp', y ='Fp1')
#sns.lineplot(ax=axes[2,0], data = df_merge, x= 'Timestamp', y ='Fp2')
#sns.lineplot(ax=axes[2,1], data = df_merge, x= 'Timestamp', y ='AF7')
#sns.lineplot(ax=axes[2,2], data = df_merge, x= 'Timestamp', y ='AF8')

#df2 = df_merge.melt(id_vars=['Timestamp'],value_vars=[])
#g = sns.FacetGrid(data=df2,col='variable',col_wrap=4)
#g.map(sns.lineplot,'Timestamp','Value')





plt.show()
