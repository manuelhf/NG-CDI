import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy import *
import math

##
# This file is just for plotting!! No real analysis happening here

dayDiff = 3 # in days

plt.figure(figsize = (5,3), dpi = 300)
ycoords = 0
allSources = np.loadtxt('allSources5G.txt')
print(len(allSources))
run = 1
allSources = allSources[75:100]
# run = 2
# allSources = allSources[120:240]
# run = 3
# allSources = allSources[240:]

for source in allSources:
    df = pd.read_csv('savingBySource5G/' + str(int(source)) + '_allAlarms.csv')

    colours = ['#2ca25f','#8856a7', 'black', 'red', 'brown', 'cyan']
    colourId = 0

    toSelect = ['Inter-System Communication Failure', 'RF Unit CPRI Interface Error']

    df = df[['name', 'dayOcc']]

    for name in np.unique(df['name'].values):
        if name in toSelect:
            dfHere = df[df['name'] == name]
            xcoords = dfHere['dayOcc'].values
            plt.scatter(xcoords,np.array([ycoords]*len(xcoords)),color = 'red', alpha = 0.4, marker = 's')
            # for xc in xcoords:
            #     plt.axvline(x = xc,color = 'red', alpha = 0.8, linewidth = 3)
        else:
            dfHere = df[df['name'] == name]
            xcoords = dfHere['dayOcc'].values
            plt.scatter(xcoords, np.array([ycoords] * len(xcoords)), color='blue', alpha = 0.4, marker = 's')
            # for xc in xcoords:
            #     plt.axvline(x=xc, color='blue', alpha=0.6, linewidth=3)
    ycoords += 1

plt.grid()
plt.title('blue alarms = features, red = targets')
plt.ylim((0,25))
plt.xlim((0,100))
plt.ylabel('Base-station ID')
plt.xlabel('days since first alarm')
# plt.savefig('alarmOccr_' + str(run) + 'RANpresentation.png',bbox_inches = 'tight')
# plt.savefig('alarmOccr_' + str(run) + '.png',bbox_inches = 'tight')
plt.show()