import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import zscore

def drop_zscore(data, thresh = 10):
  z_scores = zscore(data)
  return data[np.abs(z_scores) <= thresh]

def parse_shit_number(data):
  data = data.astype(str).str\
    .replace(r"±[\d,.]+", "", regex=True)\
    .replace(r"\[\d+\]", "", regex=True)
  data = data[~data.str.contains(r'^[\d,.]+\+[\d,.]+−[\d,.]+$')]
  return pd.to_numeric(data, errors='coerce').dropna()

# Exoplanet Attributes: IBHL Collaborative Project
fig, ax = plt.subplots(2, 3)
fig.subplots_adjust(wspace=0.5, hspace=0.5)
df = pd.read_csv('exoplanets.csv')

# Bar Graph of Length of Year
year_len = parse_shit_number(df['Period (days)'])
year_len = drop_zscore(drop_zscore(drop_zscore(drop_zscore(drop_zscore(year_len, 1), 1), 1), 1), 1)
ax[0][0].hist(year_len, bins=50)
ax[0][0].set_title('Length of Year')
ax[0][0].set_xlabel('Period (days)')
ax[0][0].set_ylabel('Number of exoplanets')
ax[0][0].grid(axis='y')

# Pie Chart of Discovery Method
disc_methd = df['Discovery method'].value_counts()
ax[0][1].pie(disc_methd)
ax[0][1].legend(
  [f'({ratio * 100:.1f}%) {label}' for label, ratio in zip(disc_methd.keys(), disc_methd / disc_methd.sum())], title='Categories',
  loc='upper left',
  bbox_to_anchor=(1, 1)
)
ax[0][1].set_title('Discovery Method')

# Line Graph of Mass vs. Host Star Mass
mass_df = df[
  ~df['Mass (MJ)'].astype(str).str.contains(r'^[\d,.]+\+[\d,.]+−[\d,.]+$') &
  ~df['Host star mass (M☉)'].astype(str).str.contains(r'^[\d,.]+\+[\d,.]+−[\d,.]+$')
]
mass_df['Mass (MJ)'] = pd.to_numeric(
  mass_df['Mass (MJ)']
    .astype(str).str
    .replace(r"±[\d,.]+", "", regex=True)
    .replace(r"\[\d+\]", "", regex=True),
  errors='coerce'
)
mass_df['Host star mass (M☉)'] = pd.to_numeric(
  mass_df['Host star mass (M☉)']
    .astype(str).str
    .replace(r"±[\d,.]+", "", regex=True)
    .replace(r"\[\d+\]", "", regex=True),
  errors='coerce'
)
mass_df = mass_df.dropna(subset=['Mass (MJ)', 'Host star mass (M☉)'])

mass = mass_df['Mass (MJ)']
host_mass = mass_df['Host star mass (M☉)']
z_scores_1 = np.abs(zscore(mass))
z_scores_2 = np.abs(zscore(host_mass))
mass = mass[(z_scores_1 <= 1) | (z_scores_2 <= 1)]
host_mass = host_mass[(z_scores_1 <= 1) | (z_scores_2 <= 1)]

m, b = np.polyfit(host_mass, mass, 1)
ax[1][0].scatter(host_mass, mass)
ax[1][0].plot(host_mass, m * host_mass + b)
ax[1][0].set_title('Host Mass v. Mass')
ax[1][0].set_xlabel('Host Star Mass')
ax[1][0].set_ylabel('Mass of Exoplanet')

# box plot of Distance (ly)
dist_ly = parse_shit_number(df['Distance (ly)'])
ax[1][1].boxplot(dist_ly)
ax[1][1].set_title('Box Plot of Distance from Earth')
ax[1][1].set_ylabel('Distance (light years)')
ax[1][2].boxplot(drop_zscore(dist_ly, 1))
ax[1][2].set_title('Box Plot of Distance from Earth')
ax[1][2].set_ylabel('Distance (light years)')

ax[0][2].set_visible(False)

fig.tight_layout()
fig.show()

input("press any key to close")