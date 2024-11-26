import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import zscore

def drop_zscore(data, thresh = 10):
  z_scores = zscore(data)
  return data[np.abs(z_scores) <= thresh]

# Exoplanet Attributes: IBHL Collaborative Project
fig, ax = plt.subplots(2, 2)
df = pd.read_csv('exoplanets.csv')

year_len = df['Period (days)'].astype(str).str.replace(r"±[\d,.]+", "", regex=True)
year_len = year_len[~year_len.str.contains(r'^[\d,.]+\+[\d,.]+−[\d,.]+$')].astype(np.float32).dropna()
year_len = drop_zscore(drop_zscore(drop_zscore(drop_zscore(drop_zscore(year_len, 1), 1), 1), 1), 1)

ax[0][0].hist(year_len, bins=50)
ax[0][0].set_title('Length of Year')
ax[0][0].set_xlabel('Period (days)')
ax[0][0].set_ylabel('Number of exoplanets')
ax[0][0].grid(axis='y')


fig.tight_layout()
fig.show()

input("press any key to close")