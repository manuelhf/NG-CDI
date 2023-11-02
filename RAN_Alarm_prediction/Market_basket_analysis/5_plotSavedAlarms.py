import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy import *
import math

dayDiff = 3 # in days

plt.figure(figsize = (5,3), dpi = 300)
ycoords = 0
allSources = np.loadtxt('allSources.txt')
print(len(allSources))
run = 1
allSources = allSources[75:100]
# run = 2
# allSources = allSources[120:240]
# run = 3
# allSources = allSources[240:]

for source in allSources:
    df = pd.read_csv('savingBySource/' + str(int(source)) + '_allAlarms.csv')

    colours = ['#2ca25f','#8856a7', 'black', 'red', 'brown', 'cyan']
    colourId = 0

    toSelect = ['Ethernet Link Fault','RF Out of Service','RF Unit VSWR Threshold Crossed','Cell Capability Degraded','Inter-System Communication Failure','RF Unit CPRI Interface Error','ALD Maintenance Link Failure','ALD Hardware Fault',' BBU Board Maintenance Link Failure',' RF Unit Hardware Fault',' RF Unit Optical Module Fault']

    df = df[['name', 'dayOcc']]

    # while True:
    #     diffs = df.dayOcc.diff().values
    #     where_are_NaNs = isnan(diffs)
    #     diffs[where_are_NaNs] = 0
    #
    #     print(diffs)
    #
    #     toRemove = []
    #     for i in range(len(diffs)):
    #         if i < len(diffs) - 1:
    #             if diffs[i] > dayDiff and diffs[i+1] > dayDiff:
    #                 toRemove.append(i)
    #         else:
    #             if diffs[i] > dayDiff:
    #                 toRemove.append(i)
    #
    #     if len(toRemove) == 0:
    #         break
    #     df = df.drop(toRemove).reset_index(drop = True)
    #
    # print('out')

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
plt.savefig('alarmOccr_' + str(run) + 'RANpresentation.png',bbox_inches = 'tight')
# plt.savefig('alarmOccr_' + str(run) + '.png',bbox_inches = 'tight')
# plt.show()