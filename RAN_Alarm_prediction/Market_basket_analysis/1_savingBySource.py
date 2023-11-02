import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori, association_rules
import matplotlib.pyplot as plt

from collections import Counter

import warnings
# from pandas.core.common import SettingWithCopyWarning
#
# warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

dayDiff = 10

# toSelect = ['Ethernet Link Fault','RF Out of Service','RF Unit VSWR Threshold Crossed','Cell Capability Degraded','Inter-System Communication Failure','RF Unit CPRI Interface Error','ALD Maintenance Link Failure','ALD Hardware Fault',' BBU Board Maintenance Link Failure',' RF Unit Hardware Fault',' RF Unit Optical Module Fault']
toSelect = ['Inter-System Communication Failure', 'RF Unit CPRI Interface Error']

allAlarms = pd.read_csv('preprocessed_5G.csv')

print(len(allAlarms))

allAlarms['occurred_on_nt'] = pd.to_datetime(allAlarms['occurred_on_nt'], format='%Y-%m-%d %H:%M:%S')
allAlarms['occurred_on_nt'] = allAlarms['occurred_on_nt'].dt.date
allAlarms = allAlarms.drop_duplicates(keep = 'last')
allAlarms = allAlarms.sort_values(['alarm_source', 'occurred_on_nt'], ascending=[True, True]).reset_index(drop=True)

allSources = np.unique(allAlarms['alarm_source'].values)
SourcesSaved = []
finalAlarmsLs = []

totalSources = 0
flag = 'go'

allAlarmsList = np.array(['RF Unit Maintenance Link Failure'])

print(len(allAlarms))

for source in allSources:
    # print('source: ', source)
    toSave = allAlarms[allAlarms['alarm_source'] == source]
    if len(toSave[toSave['name'].isin(toSelect)]) > 0:
        while True:
            toSave['diff'] = toSave['occurred_on_nt'].diff().fillna(pd.Timedelta(seconds=0)) / (
                        np.timedelta64(1, 's') * 60 * 60 * 24)

            toCheck = toSave[toSave['diff'] <= 1]
            toSave = toSave[toSave['diff'] > 1]

            toCheck = toCheck.drop_duplicates(['name']).reset_index(drop=True)
            toSave = pd.concat([toSave, toCheck]).reset_index(drop = True)

            if len(toSave) == 0:
                flag = 'out'
                break

            toSave = toSave.sort_values(['occurred_on_nt'], ascending = ['True']).reset_index(drop = True)
            diffs = toSave['diff'].values
            idtoDrop = []

            for i in range(len(diffs)):
                if i < len(diffs) - 1:
                    if diffs[i] > dayDiff and diffs[i + 1] > dayDiff:
                        idtoDrop.append(i)
                else:
                    if diffs[i] > dayDiff:
                        idtoDrop.append(i)

            if len(idtoDrop) == 0:
                break

            toSave = toSave.drop(idtoDrop).reset_index(drop=True)

            if len(toSave) == 0:
                flag = 'out'
                break

        if flag == 'out':
            continue

        diff_toappend = []
        curDiff = 0

        for diff in diffs:
            curDiff += diff
            diff_toappend.append(int(curDiff))

        toSave['dayOcc'] = np.array(diff_toappend)

        toSave = toSave[['severity', 'dayOcc', 'name']]
        toSave = toSave.drop_duplicates().reset_index(drop = True)

        if len(toSave) < 15:
            continue

        if len(np.unique(toSave['name'].values)) <= 5:
            continue

        if np.max(toSave['dayOcc'].values) < 20:
            continue

        allAlarmsList = np.concatenate((allAlarmsList,np.unique(toSave['name'].values)))
        allAlarmsList = np.unique(allAlarmsList)
        # print(len(allAlarmsList))

        finalAlarmsLs = finalAlarmsLs + toSave['name'].tolist()
        toSave.to_csv('savingBySource5G/' + str(source) + '_allAlarms.csv', index = False)
        SourcesSaved.append(source)
        totalSources += 1
    if flag == 'stop':
        break

# for al in allAlarmsList:
#     print('\'' + str(al) + '\',')

np.savetxt('allSources5G.txt', np.array(SourcesSaved))

print(len(set(finalAlarmsLs)))
print(Counter(finalAlarmsLs))

colours = ['blue','brown','orange','green','pink', 'grey','red','olive','purple','black','blue','brown','orange','green','pink','grey','red','olive','purple','cyan']

plt.figure(dpi = 300)
plt.rc('axes', axisbelow=True)
plt.grid()
barlist = plt.bar([1,2,3,4,5,6,7,8,9,10],[417,194,157,153,153,139,134,122,112,105], alpha = 0.9)
for i in range(10):
    barlist[i].set_color(colours[i])
plt.ylabel('Alarm count')
plt.savefig('alarmTopCounts.png', bbox_inches = 'tight')
print(totalSources)