import pandas as pd
import numpy as np

df = pd.read_csv('preprocessed_4G.csv')
print(len(df))
df = df.head(62000)
for i in np.unique(df['alarm_source'].values):
    print(int(i))