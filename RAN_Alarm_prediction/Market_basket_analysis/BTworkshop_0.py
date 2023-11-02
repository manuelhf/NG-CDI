import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori, association_rules
import matplotlib.pyplot as plt
import csv

import warnings
# from pandas.core import SettingWithCopyWarning

# warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

from collections import Counter

alarmsToChuck = ['User Plane Path Fault','IP PM Activation Failure','gNodeB X2 Interface Fault','Burglar Alarm', 'Inter-System Board Object Configuration Conflict', 'SCTP Link IP Address Unreachable', 'X2 Interface Fault', 'SCTP Link Fault', 'Cell RX Channel Interface Noise Power Unbalance', 'Cell PCI Conflict', 'External Clock Reference Problem', 'Time Synchronization Failure', 'External Clock Reference Not Configured', 'IP Clock Link Failure', 'Base Station Being Attacked' ,'IP Address Conflict', 'Inter-system Board Installation and Configuration Mismatch', 'LTE Availability','No License Running in System','Certificate Invalid']

## With new data

# chunksize = 8224743
# allAlarms = pd.DataFrame()
#
# for chunk in pd.read_csv('Data_clean.csv', chunksize=chunksize, ):
#     chunk = chunk.drop(chunk.columns[0], axis=1)
#     chunk = chunk[chunk['NE Type'].notna()]
#     chunk = chunk[chunk['NE Type'].str.contains("5G")]
#     allAlarms = pd.concat([allAlarms, chunk])
#     break
#
# allAlarms = allAlarms.reset_index(drop = True)
# allAlarms = allAlarms[~allAlarms['Name'].isin(alarmsToChuck)]
# allAlarms = allAlarms.reset_index(drop = True)
#
# print(allAlarms)
# print(allAlarms.columns)
#
# allAlarms.to_csv('Data_clean_updated.csv', index = False)

allAlarms = pd.read_csv('Data_clean_updated.csv')

allAlarms = allAlarms.drop(['Location Information'], axis=1) # Removing location information as now we are not removing alarms from the same board type

allAlarms = allAlarms[~allAlarms['Alarm Source'].isin(['The device is deleted'])]
allAlarmsDST = allAlarms[allAlarms['Occurred On (NT)'].str.contains("DST")]
allAlarmsRest = allAlarms[~allAlarms['Occurred On (NT)'].str.contains("DST")]


allAlarmsDST['Occurred On (NT)'] = allAlarmsDST['Occurred On (NT)'].str.replace("DST", "")
allAlarmsDST['Occurred On (NT)'] = pd.to_datetime(allAlarmsDST['Occurred On (NT)'], format='mixed', dayfirst=False)
allAlarmsDST['Occurred On (NT)'] = allAlarmsDST['Occurred On (NT)'].dt.date

allAlarmsRest['Occurred On (NT)'] = pd.to_datetime(allAlarmsRest['Occurred On (NT)'], format='mixed', dayfirst=True)
allAlarmsRest['Occurred On (NT)'] = allAlarmsRest['Occurred On (NT)'].dt.date

allAlarms = pd.concat([allAlarmsDST,allAlarmsRest])
allAlarms = allAlarms.sort_values('Occurred On (NT)')
allAlarms = allAlarms.reset_index(drop = True)

print(allAlarms.head())
print(allAlarms['Occurred On (NT)'].head())

toSelect = ['Inter-System Communication Failure', 'RF Unit CPRI Interface Error']

targets = allAlarms[allAlarms['Name'].isin(toSelect)]
targets = targets.drop_duplicates(keep = 'last')
targets['Severity'] = np.array(['critical']*len(targets))

allAlarms = allAlarms[~allAlarms['Name'].isin(toSelect)]
allAlarms = allAlarms.drop_duplicates(keep = 'last')
allAlarms['Severity'] = np.array(['minor']*len(allAlarms))

allAlarms = pd.concat([allAlarms,targets])
allAlarms = allAlarms.sort_values(['Alarm Source', 'Occurred On (NT)'], ascending=[True, True]).reset_index(drop=True)
allAlarms['Alarm Source'] = allAlarms['Alarm Source'].map(lambda x: x.rstrip('N'))

print(allAlarms.columns)
allAlarms.columns = ['alarm_source', 'name', 'occurred_on_nt', 'severity', 'ne_type']
print(allAlarms.columns)

allAlarms[['alarm_source']] = allAlarms[['alarm_source']].astype(int)

allAlarms.to_csv('preprocessed_5G.csv',index = False)