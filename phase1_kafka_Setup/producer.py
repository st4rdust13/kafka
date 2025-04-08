import pandas as pd
import time
import json
import logging
from kafka import KafkaProducer

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load dataset
df = pd.read_csv("AirQualityUCI.csv", sep=';', decimal=',', usecols=range(15))
df = df.dropna(how='all')  # drop rows where all values are NaN
df.replace(-200, pd.NA, inplace=True)  # handle missing values

# Impute missing values with forward fill (or customize)
df.fillna(method='ffill', inplace=True)

# Kafka Producer setup
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

topic = 'air_quality_data'

# Stream data
for index, row in df.iterrows():
    message = row.to_dict()
    try:
        producer.send(topic, value=message)
        logging.info(f"Sent record {index+1}: {message}")
        time.sleep(1)  # simulate real-time hourly data
    except Exception as e:
        logging.error(f"Error sending record {index+1}: {str(e)}")

producer.flush()