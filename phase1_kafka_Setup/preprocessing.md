# Data Preprocessing Strategy

## Problem
The UCI Air Quality dataset contains missing values marked as `-200`, which must be handled before streaming into Kafka.

## Approach
1. Replace all `-200` values with `NaN` using `df.replace(-200, pd.NA)` in `producer.py` 
2. Use forward fill (`fillna(method='ffill')`) to impute missing values based on previous valid observations.
3. Ensure no completely empty rows remain using `df.dropna(how='all')`.

## Justification
- Forward fill fills missing values using the most recent valid value from earlier rows. This is good for time series data where pollutant levels change gradually. 
- It prevents artificial spikes that may arise from mean or median imputation.
- It is simple and computationally efficient for real-time streaming contexts.

## Implementation
The preprocessing is implemented in the `producer.py` script to ensure clean data is streamed to Kafka.
