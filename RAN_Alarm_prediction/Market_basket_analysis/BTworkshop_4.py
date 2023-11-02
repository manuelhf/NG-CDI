import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
import pickle

pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 100)
pd.set_option('display.width', 200)

np.random.seed(27)

daysGap = 7 # ensure this is same as file BTworkshop_1

# toSelect = ['Inter-System Communication Failure', 'RF Unit CPRI Interface Error']
toSelect = ['RF Unit CPRI Interface Error']
# toSelect = ['Inter-System Communication Failure']

rulesDF = pd.read_csv('MBA_5G_daysGap_' + str(daysGap) + '_new.csv')
# rulesDF['lift'] -= rulesDF['lift'].min()
# rulesDF['lift'] /= rulesDF['lift'].max()
# rulesDF['lift'] = rulesDF['lift'].apply(lambda x: x*10)
# rulesDF['lift'] = rulesDF['lift'].round(1)

allSources = np.loadtxt('allSources5G.txt')

TPAll = 0
FPAll = 0
TNAll = 0
FNAll = 0

# print(len(sourcesConsidered))
count = 0
for source in allSources[int(len(allSources)*0.75):]:
    # print(count)
    count += 1
    # print("")
    # print("-------------------------Base Station: " + str(source)+ '-------------------------')
    # print("")
    baseStnDF = pd.read_csv('savingBySource5G/' + str(int(source)) + '_allAlarms.csv')
    maxDays = np.amax(baseStnDF['dayOcc'].values)
    ulim = daysGap
    llim = ulim - daysGap
    win = 0
    prevPredict = [] # This can only be a critical alarm
    while True:
        # print("")
        # print("Window: ", win)
        simDF = baseStnDF[baseStnDF['dayOcc'] >= llim]
        simDF = simDF[simDF['dayOcc'] <= ulim]

        win += 1
        ulim += daysGap
        llim += daysGap

        if len(simDF) < 1:
            continue

        if ulim > maxDays - daysGap:
            break

        observedAlarms = np.unique(simDF['name'].values)

        if pd.Series(prevPredict).isin(observedAlarms).any():
            TPAll += 1

        elif len(prevPredict) > 0:
            FPAll += 1

        elif pd.Series(toSelect).isin(observedAlarms).any() and len(prevPredict) == 0:
            FNAll += 1

        else:
            TNAll += 1

        predicteddf = pd.DataFrame()
        for alarm in observedAlarms:
            rulesDFhere = rulesDF[rulesDF['antecedents'].str.contains(alarm)]
            predicteddf = pd.concat([predicteddf,rulesDFhere]).drop_duplicates()

        # print(predicteddf)
        predicteddf = predicteddf[predicteddf['confidence'] >= 0.1]

        prevPredict = predicteddf['consequents'].tolist()

        # print(predicteddf)
        # print(observedAlarms)
    # break

        # rulesDF = rulesDF[pd.DataFrame(rulesDF.antecedents.tolist()).isin(observedAlarms).any(1).values]
        # print("")
        # print("percentage correct predicted = ", int((predictedCor/totalObs)*100))
        # print("")
        # if len(predictedDF) > 0:
        #     # print("PREDICTED ALARMS:")
        #     predictedDF = predictedDF.drop_duplicates(subset = ['consequents'])
        #     prevPredict = predictedDF['consequents'].values.astype(list)
        #     predictedDF = predictedDF.sort_values(['lift'], ascending = False)
        #     predAlarms = predictedDF['consequents'].values
        #     redLift = predictedDF['lift'].values
        #     for i in range(len(predAlarms)):
        #         print('URGENCY: ' + str(redLift[i]) + ' ALARM: ' + predAlarms[i])
        #         if i > 4:
        #             break
        # print(simDF)

total = TPAll + FPAll + FNAll + TNAll

print('TPAll', np.around(TPAll/total,2))
print('FPAll', np.around(FPAll/total,2))
print('FNAll', np.around(FNAll/total,2))
print('TNAll', np.around(TNAll/total,2))