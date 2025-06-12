import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV with anomaly labels
df = pd.read_csv(r'C:\Users\rehan\Desktop\ByteProbe\file_timestamps_with_anomalies.csv')

# Make sure the 'Modified' column exists and convert to datetime
df['Modified'] = pd.to_datetime(df['Modified'], errors='coerce')

# Filter data
normal = df[df['anomaly'] == -1]
anomalies = df[df['anomaly'] == 1]

# Plot anomalies over time
plt.figure(figsize=(12, 6))
plt.scatter(normal['Modified'], [0]*len(normal), color='green', label='Normal', alpha=0.6)
plt.scatter(anomalies['Modified'], [1]*len(anomalies), color='red', label='Anomaly', alpha=0.8)

plt.xlabel('Modified Timestamp')
plt.ylabel('Anomaly Indicator')
plt.title('Anomaly Detection in File Modified Timestamps')
plt.legend()
plt.tight_layout()
plt.show()
