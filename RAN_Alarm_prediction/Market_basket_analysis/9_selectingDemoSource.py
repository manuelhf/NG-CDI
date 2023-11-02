import pandas as pd
import numpy as np

allSources = np.loadtxt('allSources.txt')

analysis = pd.DataFrame(columns = ['source','len','meanDiff'])

for source in allSources:
    df = pd.read_csv('savingBySource/' + str(int(source)) + '_allAlarms.csv')
    if len(df) < 25:
        continue
    df['diff'] = df['dayOcc'].diff()
    df = df.dropna()
    diffs = df['diff'].values
    analysis.loc[len(analysis)] = [source,len(df),np.mean(diffs)]

print(analysis.sort_values(['meanDiff', 'len'], ascending=[False, False]).reset_index(drop=True))