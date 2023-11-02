import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori, association_rules
import matplotlib.pyplot as plt
import csv

import warnings
# from pandas.core.common import SettingWithCopyWarning

# warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

from collections import Counter

# allAlarmsList = [' FAN',
# ' FMU',
# ' LBBP',
# ' LRFU',
# ' LRRU',
# ' MRFU',
# ' MRRU',
# ' PMU',
# ' TCU',
# ' UBBP',
# ' UBBP-W',
# ' UBRI',
# ' UMPT',
# ' UNKNOWN',
# ' UPEU',
# 'ALD Hardware Fault',
# 'ALD Maintenance Link Failure',
# 'Automatic Version Rollback',
# 'BBU Board Maintenance Link Failure',
# 'Board Type and Configuration Mismatch',
# 'Board in Wrong Slot',
# 'Cabinet Capability  Mismatch',
# 'Cell Capability Degraded',
# 'Cell RX Channel Interference Noise Power Unbalanced',
# 'Data Configuration Exceeding Licensed Limit',
# 'Ethernet Link Fault',
# 'Extend Alarm',
# 'Inter-System Board Installation and Configuration Mismatch',
# 'Inter-System Cabinet Configuration Conflict',
# 'Inter-System Communication Failure',
# 'Local User Consecutive Login Retries Failed',
# 'MAC Excessive Frame Error Rate',
# 'MRFU',
# 'Main Control Board in Wrong Slot',
# 'RAT Conflict between separate-MPT Boards',
# 'RET Antenna Data Loss',
# 'RET Antenna Motor Fault',
# 'RET Antenna Not Calibrated',
# 'RF Out of Service',
# 'RF Unit CPRI Interface Error',
# 'RF Unit VSWR Threshold Crossed',
# 'RRU Cascading Levels and Configuration Mismatch',
# 'RRU Network Topology Type and Configuration Mismatch',
# 'Remote Maintenance Link Running Data and Configuration Mismatch',
# 'SCTP Link Congestion',
# 'Subrack Type and Configuration Mismatch',
# 'System Clock Unlocked',
# 'TMA Running Data and Configuration Mismatch']

alarmsToChuck = ['Burglar Alarm', 'Inter-System Board Object Configuration Conflict', 'SCTP Link IP Address Unreachable', 'X2 Interface Fault', 'SCTP Link Fault', 'Cell RX Channel Interface Noise Power Unbalance', 'Cell PCI Conflict', 'External Clock Reference Problem', 'Time Synchronization Failure', 'External Clock Reference Not Configured', 'IP Clock Link Failure', 'Base Station Being Attacked' ,'IP Address Conflict', 'Inter-system Board Installation and Configuration Mismatch', 'LTE Availability','No License Running in System','Certificate Invalid']
## Original code with old data
#
# allAlarms = pd.DataFrame()
#
#
# for i in range(0,11):
#     dfHere = pd.read_csv('New_data/dataRetrival_' + str(i) + '.csv')
#     allAlarms = pd.concat([allAlarms,dfHere])
#
## With new data

# chunksize = 8224743
# allAlarms = pd.DataFrame()
#
# for chunk in pd.read_csv('Data_clean.csv', chunksize=chunksize):
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

# count = 0
# features_containing_boardType = ['RF Unit DC Input Power Failure', 'RF Unit VSWR Threshold Crossed',
#                                  'RF Unit RX Channel RTWP/RSSI Too Low', 'RF Unit Hardware Fault',
#                                  'Inter-System RF Unit Parameter Settings Conflict', 'RF Unit ALD Current Out of Range',
#                                  'RF Unit Temperature Unacceptable', 'RF Unit CPRI Interface Error',
#                                  'BBU CPRI Interface Error', 'RF Unit TX Channel Gain Out of Range',
#                                  'Board Temperature Unacceptable', 'Inter-Board CANBUS Communication Failure',
#                                  'Inter-System Monitoring Device Parameter Settings Conflict',
#                                  'RF Unit ALD Switch Configuration Mismatch', 'RF Unit Overload',
#                                  'BBU CPRI Optical Module Fault', 'RF Unit Optical Module Fault', 'Board Overload',
#                                  'Transmission Optical Interface Error', 'Cabinet Air Inlet Temperature Unacceptable',
#                                  'RF Unit Optical Interface Performance Degraded','BBU CPRI Optical Module or Electrical Port Not Ready',
#                                  'RF Unit Runtime Topology Error','RF Unit Clock Problem', 'Monitoring Device Maintenance Link Failure',
#                                  'RF Unit Working Mode and Board Capability Mismatch', 'Board Not In Position', 'BBU DC Output Out of Range',
#                                  'Power Module Abnormal', 'Transmission Optical Interface Error', 'Power Module and Monitoring Module Communication Failure',
#                                  'Board Software Auto-Supply Failure', 'Inter-BBU Port Failure', 'RF Unit Software Program Error', 'BBU Fan Stalled',
#                                  'RF Unit Temperature Unacceptable', 'Board Software Synchronization Failure', 'Board Clock Input Unavailable',
#                                  'Fan Stalled', 'Board Software Program Error', 'Sensor Failure']

# toSelect = ['Ethernet Link Fault','RF Out of Service','RF Unit VSWR Threshold Crossed','Cell Capability Degraded','Inter-System Communication Failure','RF Unit CPRI Interface Error','ALD Maintenance Link Failure','ALD Hardware Fault',' BBU Board Maintenance Link Failure',' RF Unit Hardware Fault',' RF Unit Optical Module Fault']
toSelect = ['Inter-System Communication Failure', 'RF Unit CPRI Interface Error']
targets = allAlarms[allAlarms['Name'].isin(toSelect)]
targets['severity'] = np.array(['critical']*len(targets))
allAlarms = allAlarms[~allAlarms['Name'].isin(toSelect)]

allAlarms = allAlarms.drop_duplicates(keep = 'last')
allAlarms = allAlarms.sort_values(['Alarm Source', 'Occurred On (NT)'], ascending=[True, True]).reset_index(
    drop=True)

# replacementFeats = allAlarms[allAlarms.name.isin(features_containing_boardType)]
# loc_infos = replacementFeats['location_information'].values
# names = replacementFeats['name'].values
# replacedNames = []
# for i in range(len(replacementFeats)):
#     strHere = loc_infos[i]
#     strHereSplitted = strHere.split(',')
#     board = [s for s in strHereSplitted if "Board Type=" in s][0]
#     toApp = board.replace('Board Type=', '')
#     replacedNames.append(toApp)
#
# replacementFeats['name'] = np.array(replacedNames)
# allAlarms = allAlarms[~allAlarms.name.isin(features_containing_boardType)]
# allAlarms = pd.concat([allAlarms, replacementFeats])

allAlarms['Severity'] = np.array(['minor']*len(allAlarms))
allAlarms = pd.concat([allAlarms,targets])

allAlarms = allAlarms.drop_duplicates(keep = 'last')
allAlarms = allAlarms.sort_values(['Alarm Source', 'Occurred On (NT)'], ascending=[True, True]).reset_index(drop=True)
allAlarms['Alarm Source'] = allAlarms['Alarm Source'].map(lambda x: x.rstrip('N'))

print(allAlarms.columns)
allAlarms.columns = ['alarm_source', 'name', 'occurred_on_nt', 'aeverity',
       'location_information', 'ne_type', 'severity']
print(allAlarms.columns)

allAlarms[['alarm_source']] = allAlarms[['alarm_source']].astype(int)

allAlarms.to_csv('preprocessed_5G.csv',index = False)