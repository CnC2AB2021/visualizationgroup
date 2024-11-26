import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import zscore

def parse_shit_numbers(data):
  data = df['Period (days)'].astype(str).str.replace(r"±[\d,.]+", "", regex=True)
  return data[~data.str.contains(r'^[\d,.]+\+[\d,.]+−[\d,.]+$')].astype(np.float32).dropna()

def drop_zscore(data, thresh = 10):
  z_scores = zscore(data)
  return data[np.abs(z_scores) <= thresh]

# Exoplanet Attributes: IBHL Collaborative Project
fig, ax = plt.subplots(2, 2)
df = pd.read_csv('exoplanets.csv')

year_len = parse_shit_numbers(df['Period (days)'])
year_len = drop_zscore(drop_zscore(drop_zscore(drop_zscore(drop_zscore(year_len, 1), 1), 1), 1), 1)
ax[0][0].hist(year_len, bins=50)
ax[0][0].set_title('Length of Year')
ax[0][0].set_xlabel('Period (days)')
ax[0][0].set_ylabel('Number of exoplanets')
ax[0][0].grid(axis='y')

disc_methd = df['Discovery method'].value_counts()
ax[0][1].pie(disc_methd)
ax[0][1].legend(disc_methd.keys(), title='Categories', loc='upper left', bbox_to_anchor=(1, 1))
ax[0][1].set_title('Discovery Method')

fig.tight_layout()
fig.show()

input("press any key to close")