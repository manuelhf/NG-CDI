import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori, association_rules
import matplotlib.pyplot as plt

import warnings

# warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

from collections import Counter

targets = pd.read_csv('targetVar_selectedAlarms.csv', usecols=['name','alarm_source','location_information','occurred_on_nt'])
targets['occurred_on_nt'] = pd.to_datetime(targets['occurred_on_nt'], format='%Y-%m-%d %H:%M:%S')
targets['occurred_on_nt'] = targets['occurred_on_nt'].dt.date

features = pd.read_csv('featureCleanVar_selectedAlarms.csv', usecols=['name','alarm_source','location_information','occurred_on_nt'])
features['occurred_on_nt'] = pd.to_datetime(features['occurred_on_nt'], format='%Y-%m-%d %H:%M:%S')
features['occurred_on_nt'] = features['occurred_on_nt'].dt.date

allAlarms = pd.concat([targets,features])
allAlarms = allAlarms.sort_values('occurred_on_nt')

count = 0

alarmsToChuck = ['Burglar Alarm', 'Inter-System Board Object Configuration Conflict', 'SCTP Link IP Address Unreachable', 'X2 Interface Fault', 'SCTP Link Fault', 'Cell RX Channel Interface Noise Power Unbalance', 'Cell PCI Conflict', 'External Clock Reference Problem', 'Time Synchronization Failure', 'External Clock Reference Not Configured', 'IP Clock Link Failure', 'Base Station Being Attacked' ,'IP Address Conflict', 'Inter-system Board Installation and Configuration Mismatch', 'LTE Availability','No License Running in System','Certificate Invalid']
allAlarms = allAlarms[~allAlarms['name'].isin(alarmsToChuck)]

features_containing_boardType = ['RF Unit DC Input Power Failure', 'RF Unit VSWR Threshold Crossed',
                                 'RF Unit RX Channel RTWP/RSSI Too Low', 'RF Unit Hardware Fault',
                                 'Inter-System RF Unit Parameter Settings Conflict', 'RF Unit ALD Current Out of Range',
                                 'RF Unit Temperature Unacceptable', 'RF Unit CPRI Interface Error',
                                 'BBU CPRI Interface Error', 'RF Unit TX Channel Gain Out of Range',
                                 'Board Temperature Unacceptable', 'Inter-Board CANBUS Communication Failure',
                                 'Inter-System Monitoring Device Parameter Settings Conflict',
                                 'RF Unit ALD Switch Configuration Mismatch', 'RF Unit Overload',
                                 'BBU CPRI Optical Module Fault', 'RF Unit Optical Module Fault', 'Board Overload',
                                 'Transmission Optical Interface Error', 'Cabinet Air Inlet Temperature Unacceptable',
                                 'RF Unit Optical Interface Performance Degraded','BBU CPRI Optical Module or Electrical Port Not Ready',
                                 'RF Unit Runtime Topology Error','RF Unit Clock Problem', 'Monitoring Device Maintenance Link Failure',
                                 'RF Unit Working Mode and Board Capability Mismatch', 'Board Not In Position', 'BBU DC Output Out of Range',
                                 'Power Module Abnormal', 'Transmission Optical Interface Error', 'Power Module and Monitoring Module Communication Failure',
                                 'Board Software Auto-Supply Failure', 'Inter-BBU Port Failure', 'RF Unit Software Program Error', 'BBU Fan Stalled',
                                 'RF Unit Temperature Unacceptable', 'Board Software Synchronization Failure', 'Board Clock Input Unavailable',
                                 'Fan Stalled', 'Board Software Program Error', 'Sensor Failure']

toSelect = ['Ethernet Link Fault','RF Out of Service','RF Unit VSWR Threshold Crossed','Cell Capability Degraded','Inter-System Communication Failure','RF Unit CPRI Interface Error','ALD Maintenance Link Failure','ALD Hardware Fault',' BBU Board Maintenance Link Failure',' RF Unit Hardware Fault',' RF Unit Optical Module Fault']
targets = targets[targets['name'].isin(toSelect)]
targets['severity'] = np.array(['critical']*len(targets))
allAlarms = allAlarms[~allAlarms['name'].isin(toSelect)]

allAlarms = allAlarms.drop_duplicates(keep = 'last')
allAlarms = allAlarms.sort_values(['alarm_source', 'occurred_on_nt'], ascending=[True, True]).reset_index(
    drop=True)

replacementFeats = allAlarms[allAlarms.name.isin(features_containing_boardType)]
loc_infos = replacementFeats['location_information'].values
names = replacementFeats['name'].values
replacedNames = []
for i in range(len(replacementFeats)):
    strHere = loc_infos[i]
    strHereSplitted = strHere.split(',')
    board = [s for s in strHereSplitted if "Board Type=" in s][0]
    toApp = board.replace('Board Type=', '')
    replacedNames.append(toApp)

replacementFeats['name'] = np.array(replacedNames)
allAlarms = allAlarms[~allAlarms.name.isin(features_containing_boardType)]
allAlarms = pd.concat([allAlarms, replacementFeats])
allAlarms['severity'] = np.array(['minor']*len(allAlarms))
allAlarms = pd.concat([allAlarms,targets])

allAlarms = allAlarms.drop_duplicates(keep = 'last')
allAlarms = allAlarms.sort_values(['alarm_source', 'occurred_on_nt'], ascending=[True, True]).reset_index(
    drop=True)

allAlarms.to_csv('dataP1.csv', index = False)