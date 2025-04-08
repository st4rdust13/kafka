
import json
import logging
from kafka import KafkaConsumer
import joblib
import numpy as np
import pandas as pd

# Setup logging to monitor process in terminal
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the trained model
model = joblib.load('co_forecast_model.pkl')

# Define feature extraction from a record
def preprocess_record(record):
    try:
        features = {
            'Hour': int(pd.to_datetime(record['Date'] + ' ' + record['Time'], format='%d/%m/%Y %H.%M.%S').hour),
            'Day': int(pd.to_datetime(record['Date'] + ' ' + record['Time'], format='%d/%m/%Y %H.%M.%S').day),
            'Month': int(pd.to_datetime(record['Date'] + ' ' + record['Time'], format='%d/%m/%Y %H.%M.%S').month),
            'CO_lag1': float(record.get('CO(GT)', np.nan)),
            'CO_lag2': float(record.get('CO(GT)', np.nan)),  # optional fallback
            'CO_roll3': float(record.get('CO(GT)', np.nan)),
            'CO_std3': 0.0  # can’t compute std in real-time easily — set to 0 or a default
        }
        return pd.DataFrame([features])
    except Exception as e:
        logging.error(f"Error preprocessing record: {e}")
        return None

# Kafka Consumer setup
consumer = KafkaConsumer(
    'air_quality_data',  # topic name
    bootstrap_servers='localhost:9092',  # Kafka server address
    auto_offset_reset='earliest',  # Start from the beginning of the topic
    enable_auto_commit=True,  # Automatically commit offsets
    group_id='air_quality_group',  # Consumer group ID
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))  # Decode JSON messages
)

# Consuming and saving data
for message in consumer:
    record = message.value
    features_df = preprocess_record(record)
    if features_df is not None:
        prediction = model.predict(features_df)[0]
        logging.info(f"Predicted CO(GT): {prediction:.2f}")
    else:
        logging.warning("Skipping prediction due to preprocessing error.")
    try:
        # Log received message
        logging.info(f"Received record: {record}")

        # Save the record to a JSON file for analysis
        with open("received_air_quality_data.json", "a") as f:
            f.write(json.dumps(record) + "\n")

    except Exception as e:
        logging.error(f"Error processing record: {str(e)}")
