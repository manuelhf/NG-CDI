import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time

np.random.seed(27)

daysGap = 10
numSources = 100

rulesDF = pd.read_csv('MBA_daysGap_' + str(daysGap) + '_new.csv')
rulesDF['lift'] -= rulesDF['lift'].min()
rulesDF['lift'] /= rulesDF['lift'].max()
rulesDF['lift'] = rulesDF['lift'].apply(lambda x: x*10)
rulesDF['lift'] = rulesDF['lift'].round(1)

allSources = ['64078', '26829']
# allSources = ['90169']
for source in allSources:
    print("")
    print("-------------------------Base Station: " + str(source)+ '-------------------------')
    print("")
    baseStnDF = pd.read_csv('savingBySource/' + str(int(source)) + '_allAlarms.csv')
    locAlarms = baseStnDF['dayOcc'].values
    maxDays = np.amax(baseStnDF['dayOcc'].values)
    ulim = daysGap
    llim = ulim - daysGap
    win = 0

    while True:
        print("")
        print("Window: ", win)
        win += 1
        simDF = baseStnDF[baseStnDF['dayOcc'] >= llim]
        simDF = simDF[simDF['dayOcc'] <= ulim]
        alToday = simDF[simDF['dayOcc'] == ulim]

        if len(alToday) > 0:
            alHere = locAlarms[locAlarms <= ulim]
            plt.figure(figsize=(6, 2),dpi = 300)
            plt.title('Simulated Base Station: ' + source)
            plt.xlabel('Days')
            plt.scatter(alHere, [0.1] * len(alHere), color='r', alpha=0.3)
            plt.xlim(0, 100)
            plt.yticks([])
            plt.ylim(0, 0.5)
            plt.axvline(x=ulim, c='r', linewidth=3, label = 'current time-step: ' + str(win))
            plt.fill_between([ulim - daysGap, ulim], 0.3, color='black', alpha=0.4, label = 'antecedents')
            plt.fill_between([ulim, ulim + daysGap], 0.3, color='black', alpha=0.2, label = 'consequents')
            plt.legend()
            plt.show()
            # plt.savefig('gifs/gif_' + source + '_' + str(win) + '.png', bbox_inches = 'tight')
            # plt.close()

        else:
            alHere = locAlarms[locAlarms <= ulim]
            plt.figure(figsize=(6, 2), dpi = 300)
            plt.title('Simulated Base Station: ' + source)
            plt.xlabel('Days')
            plt.scatter(alHere, [0.1] *
                        len(alHere), color='r', alpha=0.3)
            plt.xlim(0, 100)
            plt.yticks([])
            plt.ylim(0, 0.5)
            plt.axvline(x=ulim, c='b', linewidth=3, label='current time-step: ' + str(win))
            plt.fill_between([ulim - daysGap, ulim], 0.3, color='black', alpha=0.4, label='antecedents')
            plt.fill_between([ulim, ulim + daysGap], 0.3, color='black', alpha=0.2, label='consequents')
            plt.legend()
            plt.show()
            # plt.savefig('gifs/gif_' + source + '_' + str(win) + '.png', bbox_inches='tight')
            # plt.close()

        ulim += 8
        llim += 8

        if len(simDF) < 1:
            continue

        if ulim > maxDays - daysGap + 1:
            break

        observedAlarms = simDF['name'].values

        predictedDF = pd.DataFrame()
        print("OBSERVED ALARMS:")
        for alarmObs in observedAlarms:
            print(alarmObs)
            rulesDFhere = rulesDF[rulesDF['antecedents'].str.contains(alarmObs)]
            predictedDF = pd.concat([predictedDF,rulesDFhere])
        # rulesDF = rulesDF[pd.DataFrame(rulesDF.antecedents.tolist()).isin(observedAlarms).any(1).values]
        print("")
        if len(predictedDF) > 0:
            print("PREDICTED ALARMS:")
            predictedDF = predictedDF.drop_duplicates(subset = ['consequents'])
            predictedDF = predictedDF.sort_values(['lift'], ascending = False)
            predAlarms = predictedDF['consequents'].values
            redLift = predictedDF['lift'].values
            for i in range(len(predAlarms)):
                print('URGENCY: ' + str(redLift[i]) + ' ALARM: ' + predAlarms[i])

        # print(simDF)