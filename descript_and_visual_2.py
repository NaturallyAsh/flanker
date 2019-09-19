import pandas as pd 
import seaborn as sns 
import numpy as np 
import matplotlib.pyplot as plt 

sns.set_style('white')
df = pd.read_csv('flanks2.csv')
# print(df)

# Lets group the data by trial type (i.e., congruent and incongruent)
grouped_df = df.groupby(['TrialType'], as_index=True).mean()
# print(grouped_df.mean())
# means = grouped_df.mean()
# print(means)
print(grouped_df.head())

# cm is the colormap and Paired is the set of colors you want.
# np.arange creates a range of colors from 0 to the len of the df.
ax = grouped_df.plot.bar(
    rot=0, 
    color=[plt.cm.Paired(np.arange(len(grouped_df)))],
    legend=False
    )
ax.set_ylabel("Reaction Time (ms)")
ax.grid(axis='y')
plt.show()

# Describe gives us some descriptive statistics
# print(grouped_df.describe().unstack())

# ax = df[['RT', 'TrialType']].plot(
#     kind='bar',
#     )
# width = 0.25
# pos = list(range(len(df['TrialType'])))
# fig, ax = plt.subplots(figsize=(10,5))

# plt.bar(
#     pos,
#     df['TrialType'],
#     width,
#     alpha=0.5
#     )

# plt.bar([p + width for p in pos],
#     df['RT'],
#     width,
#     alpha=0.5
#     )

# get average for ALL TRIALS
# MAKE 2 GRAPHS; 1 bar graph w/ incongruent/congruent means (x-axis) and
# RT (y-axis). 2nd graph ...(?. corr vs. incorr? ask Dr. Briganti)




