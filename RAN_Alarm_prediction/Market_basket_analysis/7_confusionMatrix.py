import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
import pickle

np.random.seed(27)

daysGap = 10
numSources = 100

rulesDF = pd.read_csv('MBA_daysGap_' + str(daysGap) + '_new.csv')
rulesDF['lift'] -= rulesDF['lift'].min()
rulesDF['lift'] /= rulesDF['lift'].max()
rulesDF['lift'] = rulesDF['lift'].apply(lambda x: x*10)
rulesDF['lift'] = rulesDF['lift'].round(1)
# allSources = np.loadtxt('allSources.txt').astype(int)
# allSources = np.random.choice(allSources, numSources)

# allSources = ['90160','90755','61087','91492','90224','90169','90020','59337','69987','98011', '98676', '90450', '64078', '26829']
# allSources = ['90450']
with open("sourcesConsidered", "rb") as fp:
    sourcesConsidered = pickle.load(fp)

TPAll = 0
FPAll = 0
TNAll = 0
FNAll = 0

print(len(sourcesConsidered))
count = 0
for source in sourcesConsidered:
    print(count)
    count += 1
    # print("")
    # print("-------------------------Base Station: " + str(source)+ '-------------------------')
    # print("")
    baseStnDF = pd.read_csv('savingBySource/' + str(int(source)) + '_allAlarms.csv')
    maxDays = np.amax(baseStnDF['dayOcc'].values)
    ulim = daysGap
    llim = ulim - daysGap
    win = 0
    prevPredict = []
    while True:
        # print("")
        # print("Window: ", win)
        simDF = baseStnDF[baseStnDF['dayOcc'] >= llim]
        simDF = simDF[simDF['dayOcc'] <= ulim]

        win += 1
        ulim += 8
        llim += 8

        if len(simDF) < 1:
            continue

        if ulim > maxDays - daysGap:
            break

        observedAlarms = np.unique(simDF['name'].values)

        predictedCor = 0
        predictedWr = 0
        totalObs = len(observedAlarms)

        predictedDF = pd.DataFrame()
        # print("OBSERVED ALARMS:")
        for alarmPred in prevPredict:
            if alarmPred not in observedAlarms:
                FPAll += 1
        for alarmObs in observedAlarms:
            # print(alarmObs)
            if alarmObs in prevPredict:
                predictedCor += 1
                TPAll += 1
            else:
                predictedWr += 1
                FNAll += 1
            rulesDFhere = rulesDF[rulesDF['antecedents'].str.contains(alarmObs)]
            predictedDF = pd.concat([predictedDF,rulesDFhere])
        # rulesDF = rulesDF[pd.DataFrame(rulesDF.antecedents.tolist()).isin(observedAlarms).any(1).values]
        # print("")
        # print("percentage correct predicted = ", int((predictedCor/totalObs)*100))
        # print("")
        if len(predictedDF) > 0:
            # print("PREDICTED ALARMS:")
            predictedDF = predictedDF.drop_duplicates(subset = ['consequents'])
            prevPredict = predictedDF['consequents'].values.astype(list)
            predictedDF = predictedDF.sort_values(['lift'], ascending = False)
            predAlarms = predictedDF['consequents'].values
            redLift = predictedDF['lift'].values
            # for i in range(len(predAlarms)):
            #     print('URGENCY: ' + str(redLift[i]) + ' ALARM: ' + predAlarms[i])
            #     if i > 4:
            #         break
        # print(simDF)

print('TPAll', TPAll)
print('FPAll', FPAll)
print('FNAll', FNAll)