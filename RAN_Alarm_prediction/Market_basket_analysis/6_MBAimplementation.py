import pandas as pd
import seaborn as sns
import numpy as np
import pickle
import seaborn as sns
import matplotlib.pyplot as plt
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import mlxtend as ml
from sklearn.preprocessing import MultiLabelBinarizer
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori

pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 100)
pd.set_option('display.width', 200)

daysGap = 10

toSelect = ['Ethernet Link Fault','RF Out of Service','RF Unit VSWR Threshold Crossed','Cell Capability Degraded','Inter-System Communication Failure','RF Unit CPRI Interface Error','ALD Maintenance Link Failure','ALD Hardware Fault',' BBU Board Maintenance Link Failure',' RF Unit Hardware Fault',' RF Unit Optical Module Fault']

listOfAlarms = []
allSources = np.loadtxt('allSources.txt')
sourcesConsidered = []

for source in allSources:
    flag = 'in'
    df = pd.read_csv('savingBySource/' + str(int(source)) + '_allAlarms.csv')
    df['diff'] = df['dayOcc'].diff()
    df = df[df['dayOcc'] > daysGap].reset_index(drop=True)
    while True:
        initDayDiff = df['diff'].values[0]
        if initDayDiff > daysGap:
            break
        else:
            if len(df) == 1:
                flag = 'out'
                break
            df = df.iloc[1:]
    if flag == 'out':
        continue

    alarmsHereInit = df['name'].tolist()
    diffsHere = df['diff'].tolist()

    breakIds = []
    for i in range(1, len(diffsHere)):
        if diffsHere[i] > daysGap:
            breakIds.append(i)

    alarmsHere = []
    for i in breakIds:
        alarmsHere.append(alarmsHereInit[:i])
        alarmsHereInit = alarmsHereInit[i:]

    if len(alarmsHereInit) > 5:
        alarmsHere.append(alarmsHereInit)

    if len(alarmsHere) > 0:
        sourcesConsidered.append(source)
        for alarmsLs in alarmsHere:
            listOfAlarms.append(set(alarmsLs))

print(sourcesConsidered)
print(len(sourcesConsidered))

with open("sourcesConsidered", "wb") as fp:
    pickle.dump(sourcesConsidered, fp)

print(listOfAlarms)
te = TransactionEncoder()
te_ary = te.fit(listOfAlarms).transform(listOfAlarms)
df = pd.DataFrame(te_ary, columns=te.columns_)

df.to_csv('MBAdf.csv', index = False)

frequent_alarmsets = apriori(df, min_support=0.1, use_colnames=True)
frequent_alarmsets = association_rules(frequent_alarmsets, metric="lift", min_threshold=0.2)
frequent_alarmsets['rhs_items'] = frequent_alarmsets['consequents'].apply(lambda x:len(x))
frequent_alarmsets = frequent_alarmsets[frequent_alarmsets['rhs_items'] == 1]

rules = frequent_alarmsets[['antecedents','consequents','support','confidence','lift']]
rules = rules.sort_values(by = ['support'], ascending = False).reset_index(drop = True)

rules[['antecedents','consequents']] = rules[['antecedents','consequents']].astype(str)

rules['antecedents'] = rules['antecedents'].str[12:]
rules['antecedents'] = rules['antecedents'].str[:-3]

rules['consequents'] = rules['consequents'].str[12:]
rules['consequents'] = rules['consequents'].str[:-3]

# rules = rules.str.replace(['Board Type and Configuration Mismatch', 'RAT Conflict between separate-MPT Boards'],
#                      ['BTCM', 'RAT Conflict'])

# rules['antecedents'] = rules['antecedents'].replace('Board Type and Configuration Mismatch', 'BTCM', regex = True)
# rules['antecedents'] = rules['antecedents'].replace('RAT Conflict between separate-MPT Boards', 'RAT Conflict', regex = True)
# rules['antecedents'] = rules['antecedents'].replace('\' ', '', regex = True)
# rules['antecedents'] = rules['antecedents'].replace(' ', '', regex = True)
#
# rules['consequents'] = rules['consequents'].replace('Board Type and Configuration Mismatch', 'BTCM', regex = True)
# rules['consequents'] = rules['consequents'].replace('RAT Conflict between separate-MPT Boards', 'RAT Conflict', regex = True)
# rules['consequents'] = rules['consequents'].replace('\' ', '', regex = True)
# rules['consequents'] = rules['consequents'].replace(' ', '', regex = True)

print(rules.head())

print(listOfAlarms)
rules['support'] = rules['support'].round(3)
rules['confidence'] = rules['confidence'].round(3)
rules['lift'] = rules['lift'].round(3)

rules.to_csv('MBA_daysGap_' + str(daysGap) + '_new.csv',index = False)

pivot = rules.pivot(index = 'antecedents', columns = 'consequents', values= 'lift')

# plt.figure(dpi = 300)
# sns.heatmap(pivot, annot = True)
# plt.yticks(rotation=45)
# plt.xticks(rotation=90)
# plt.savefig('result_RAN.png', bbox_inches = 'tight')
# plt.show()

## Definitions:
# SUPPORT = relative frequency that the given rule shows up
# CONFIDENCE = a measure of the reliability of a given rule
# LIFT = the ratio of the observed support to that expected if the two rules were independent