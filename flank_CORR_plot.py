import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.patches as mpatches 
from matplotlib.lines import Line2D 

plt.style.use('seaborn-notebook')
# print(plt.style.available)

# need to type the whole path before filename (ie. Sept_24...) or
# trace will say file does not exist
df = pd.read_csv('/Users/macuser/Documents/PYTHON/testing/test_data_folder/Sep_24_2046.csv')

# group the data by display type (i.e., congruent and incongruent)
# grouped_df = df.groupby(['displays'], as_index=True).mean()
grouped_df = df.groupby(['displays'], as_index=True).mean()

print(grouped_df)

# select rows from df info: https://datatofish.com/select-rows-pandas-dataframe/
# con_df = grouped_df.loc[grouped_df.displays == 'congruent']
# print(con_df)

# incon_df = grouped_df.loc[grouped_df.displays == 'incongruent']
# print(incon_df)

# then, select specific column from display group (i.e. kb.rt) in order
# to only plot that column rather than all the columns
flank_groupBy = grouped_df['kb.corr']
print(flank_groupBy)
print(flank_groupBy.describe())
means = flank_groupBy.mean()
print(means)
stds = flank_groupBy.std()
print(stds)
# # cm is the colormap and Paired is the set of colors you want.
# # np.arange creates a range of colors from 0 to the len of the df.
fig, ax = plt.subplots()
# TODO: consider setting the legend to fig rather than ax
# setting it to fig puts the legend outside of the figure
ax = flank_groupBy.plot.bar(
    rot=0,
    color=plt.cm.Paired(np.arange(len(flank_groupBy))),
    legend=True
    )

# created a custom legend; not currently implemented
mean = mpatches.Patch(color='green', label=flank_groupBy.describe().loc[['mean']].to_string())
std = mpatches.Patch(color='green', label=flank_groupBy.describe().loc[['std']].to_string())

# alt method to create custom legend; currently implementing
legend_elements = [
    Line2D([0],[0], 
        marker='o', 
        color='w', 
        label=flank_groupBy.describe().loc[['mean']].to_string(), 
        markerfacecolor='k', markersize=8),
    Line2D([0],[0], 
        marker='o', 
        color='w', 
        label=flank_groupBy.describe().loc[['std']].to_string(), 
        markerfacecolor='k', markersize=8)]

# legend api @ https://matplotlib.org/3.1.1/api/legend_api.html?highlight=legend#module-matplotlib.legend
leg = ax.legend(
    handles=legend_elements,
    loc='best', 
    handlelength=1.0, 
    fancybox=True,
    ncol=2)

# the below iteration will work only if I created the custom legend
# using the 'mean' and 'std' mpatches; no effect on legend_elements
# for item in leg.legendHandles:
#     item.set_visible(False)
ax.set_ylabel('Correct')
# create a grid along the y axis; can do along this x if so choose
ax.grid(axis='y')
plt.show()