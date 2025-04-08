# Loading and parsing the data 

import json
import pandas as pd
import seaborn as sns
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt

records = []
with open('received_air_quality_data.json', 'r') as f:
    for line in f:
        try:
            records.append(json.loads(line.strip()))
        except json.JSONDecodeError:
            continue  # skip malformed lines

df = pd.DataFrame(records)

##Cleaning and ordering the data

# Combine Date & Time into a single datetime column:
df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H.%M.%S', errors='coerce')
df.set_index('Datetime', inplace=True)
df.drop(columns=['Date', 'Time'], inplace=True)

# Convert all data to numeric and fill missing values:
df = df.apply(pd.to_numeric, errors='coerce')
df.fillna(method='ffill', inplace=True)  # forward fill for time series


## Basic Visualizations 



df['CO(GT)'].plot(title="CO Concentration Over Time", figsize=(12,4))
plt.show()

df['NOx(GT)'].plot(title="NOx Concentration Over Time", figsize=(12,4))
plt.show()

df['C6H6(GT)'].plot(title="Benzene (C6H6) Concentration Over Time", figsize=(12,4))
plt.show()

#patterns
df['Hour'] = df.index.hour
df['DayOfWeek'] = df.index.dayofweek

hourly_avg = df.groupby('Hour')[['CO(GT)', 'NOx(GT)', 'C6H6(GT)']].mean()
weekly_avg = df.groupby('DayOfWeek')[['CO(GT)', 'NOx(GT)', 'C6H6(GT)']].mean()

#plots 
hourly_avg.plot(title="Average Pollutants by Hour", figsize=(10,4))
plt.show()
weekly_avg.plot(title="Average Pollutants by Day of Week", figsize=(10,4))
plt.show()

#heatmap

plt.figure(figsize=(10,8))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
plt.title("Correlation Between Pollutants")
plt.show()


##Advanced visualizations 


# Autocorrelation and Partial Autocorrelation
plot_acf(df['CO(GT)'].dropna(), title="Autocorrelation - CO")
plt.show()

plot_pacf(df['CO(GT)'].dropna(), title="Partial Autocorrelation - CO")
plt.show()

# Decomposition
decompose_result = seasonal_decompose(df['CO(GT)'].dropna(), model='additive', period=24)
decompose_result.plot()
plt.show()
