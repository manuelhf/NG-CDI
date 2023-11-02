import pandas as pd
import seaborn as sns
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import mlxtend as ml
from sklearn.preprocessing import MultiLabelBinarizer
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
import string

daysGap = 10

pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 100)
pd.set_option('display.width', 200)

df = pd.read_csv('MBAdf.csv')
print(df.head())

listToAdd = list(string.ascii_uppercase)
finalLs = []
count = 0
idx = 0
idxIn = 0
while count < len(df.columns):
    charHere = listToAdd[idx]
    finalLs.append(charHere + listToAdd[idxIn])
    count += 1
    idxIn += 1
    if count == len(listToAdd) or count == len(listToAdd)*2:
        idx += 1
        idxIn = 0

df.columns = finalLs
print(df.head())
print(finalLs)

frequent_alarmsets = apriori(df, min_support=0.1, use_colnames=True)
frequent_alarmsets = association_rules(frequent_alarmsets, metric="lift", min_threshold=2.7)
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

# print(listOfAlarms)
rules['support'] = rules['support'].round(3)
rules['confidence'] = rules['confidence'].round(3)
rules['lift'] = rules['lift'].round(3)

rules.to_csv('MBA_daysGap_' + str(daysGap) + '_new.csv',index = False)

pivot = rules.pivot(index = 'antecedents', columns = 'consequents', values= 'lift')

plt.figure(figsize=(3,10),dpi = 300)
sns.heatmap(pivot, annot = True)
plt.yticks(rotation=45)
plt.xticks(rotation=90)
plt.savefig('result_RAN.png', bbox_inches = 'tight')
plt.show()

## Definitions:
# SUPPORT = relative frequency that the given rule shows up
# CONFIDENCE = a measure of the reliability of a given rule
# LIFT = the ratio of the observed support to that expected if the two rules were independent