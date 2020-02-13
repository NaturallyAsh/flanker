import pandas as pd 

dfA = pd.read_csv('/Users/macuser/Documents/PYTHON/testing/pandas_data_testing/SubID-2342-Jan_31_1323.csv', sep=',')

rtA = dfA['kb.rt'].mean()
print(rtA)

dfB = pd.read_csv('/Users/macuser/Documents/PYTHON/testing/pandas_data_testing/SubID-2398-Jan_31_1325.csv', sep=',')

rtB = dfB['kb.rt'].mean()
print(rtB)

dfC = pd.read_csv('/Users/macuser/Documents/PYTHON/testing/pandas_data_testing/SubID-2342-Jan_31_1329.csv', sep=',')

rtC = dfC['kb.rt'].mean()
print(rtC)

# combine the three group rt datasets into a separate dataframe

frames = [dfA, dfB, dfC]
# 'keys' arg assigns labels to each concated df
frames_conc = pd.concat(frames, keys=['A', 'B', 'C'])
print(frames_conc)

# YAY! df.drop() drops specified columns
# doc: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.drop.html
# print(frames_conc.drop(columns=['condsFile']))
dropped = frames_conc.drop(columns=[
    'condsFile',
    'blocks.thisRepN',
    'blocks.thisN',
    'trials.thisRepN',
    'date'])
print(dropped)
# drop columns where at least one ele is missing
print(dropped.dropna(axis='columns'))
print(dropped.describe())