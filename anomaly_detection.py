import pandas as pd
from sklearn.ensemble import IsolationForest
from datetime import datetime

# Load CSV file (update path if needed)
csv_path = r"C:\Users\rehan\Desktop\ByteProbe\file_timestamps.csv"
df = pd.read_csv(csv_path)

# Convert timestamp columns to datetime
# Adjust column names to your CSV headers exactly
df['Created'] = pd.to_datetime(df['Created'], errors='coerce')
df['Modified'] = pd.to_datetime(df['Modified'], errors='coerce')
df['Accessed'] = pd.to_datetime(df['Accessed'], errors='coerce')

# Feature engineering: convert datetime to Unix timestamp (float)
df['created_ts'] = df['Created'].apply(lambda x: x.timestamp() if pd.notnull(x) else 0)
df['modified_ts'] = df['Modified'].apply(lambda x: x.timestamp() if pd.notnull(x) else 0)
df['accessed_ts'] = df['Accessed'].apply(lambda x: x.timestamp() if pd.notnull(x) else 0)

# Optional: Add difference features
df['mod_create_diff'] = df['modified_ts'] - df['created_ts']
df['acc_create_diff'] = df['accessed_ts'] - df['created_ts']

# Select features for model
features = ['created_ts', 'modified_ts', 'accessed_ts', 'mod_create_diff', 'acc_create_diff']
X = df[features].fillna(0)

# Initialize and train Isolation Forest
model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
model.fit(X)

# Predict anomalies (-1 is anomaly, 1 is normal)
df['anomaly'] = model.predict(X)

# Anomaly score (the lower, the more anomalous)
df['anomaly_score'] = model.decision_function(X)

# Save results with anomaly flags
output_path = r"C:\Users\rehan\Desktop\ByteProbe\file_timestamps_with_anomalies.csv"
df.to_csv(output_path, index=False)

print(f"✅ Anomaly detection done! Results saved to: {output_path}")
