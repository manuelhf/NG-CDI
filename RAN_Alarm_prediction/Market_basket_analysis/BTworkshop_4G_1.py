import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori, association_rules
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

from collections import Counter

import warnings
# from pandas.core.common import SettingWithCopyWarning
#
# warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

dayDiff = 7

toSelect = ['Ethernet Link Fault','RF Out of Service','RF Unit VSWR Threshold Crossed','Inter-System Communication Failure','RF Unit CPRI Interface Error','ALD Maintenance Link Failure','ALD Hardware Fault']

allAlarms = pd.read_csv('preprocessed_4G.csv')

# print(allAlarms.head())

alarmstotal = np.unique(allAlarms['name'].values)
print(len(alarmstotal))

allAlarms['occurred_on_nt'] = pd.to_datetime(allAlarms['occurred_on_nt'], format='%Y-%m-%d')
allAlarms['occurred_on_nt'] = allAlarms['occurred_on_nt'].dt.date
allAlarms = allAlarms.drop_duplicates(keep = 'last')
allAlarms = allAlarms.sort_values(['alarm_source', 'occurred_on_nt'], ascending=[True, True]).reset_index(drop=True)

allSources = np.unique(allAlarms['alarm_source'].values)
print(len(allSources))

SourcesSaved = []
finalAlarmsLs = []

totalSources = 0
flag = 'go'

allAlarmsList = np.array(['Remote Maintenance Link Failure'])

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

            toSave = toSave.sort_values(['occurred_on_nt'], ascending = True).reset_index(drop = True)
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
            flag = 'go'
            continue

        diff_toappend = []
        curDiff = 0

        for diff in diffs:
            curDiff += diff
            diff_toappend.append(int(curDiff))

        toSave['dayOcc'] = np.array(diff_toappend)

        toSave = toSave[['severity', 'dayOcc', 'name']]
        toSave = toSave.drop_duplicates().reset_index(drop = True)

        # if len(toSave) < 5:
        #     continue

        if len(np.unique(toSave['name'].values)) <= 2:
            continue

        # if np.max(toSave['dayOcc'].values) < 5:
        #     continue

        allAlarmsList = np.concatenate((allAlarmsList,np.unique(toSave['name'].values)))
        allAlarmsList = np.unique(allAlarmsList)

        finalAlarmsLs = finalAlarmsLs + toSave['name'].tolist()
        toSave.to_csv('savingBySource4G/' + str(source) + '_allAlarms.csv', index = False)
        SourcesSaved.append(source)
        totalSources += 1
    if flag == 'stop':
        break


np.savetxt('allSources4G.txt', np.array(SourcesSaved))

print(totalSources)
print(len(set(finalAlarmsLs)))
print(Counter(finalAlarmsLs))

word_counter = {}
for word in finalAlarmsLs:
    if word in word_counter:
        word_counter[word] += 1
    else:
        word_counter[word] = 1

popular_alarms = sorted(word_counter, key = word_counter.get, reverse = True)

last_40 = popular_alarms[-40:]
print(last_40)

colours = ['blue','brown','orange','green','pink', 'grey','red','olive','purple','black','blue','brown','orange','green','pink','grey','red','olive','purple','cyan']

# plt.figure(dpi = 300)
# plt.rc('axes', axisbelow=True)
# plt.grid()
# barlist = plt.bar([1,2,3,4,5,6,7,8,9,10],[417,194,157,153,153,139,134,122,112,105], alpha = 0.9)
# for i in range(10):
#     barlist[i].set_color(colours[i])
# plt.ylabel('Alarm count')
# plt.savefig('alarmTopCounts.png', bbox_inches = 'tight')
# print(totalSources)