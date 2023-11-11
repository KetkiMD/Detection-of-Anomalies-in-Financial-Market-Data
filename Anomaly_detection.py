import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

data = yf.download('AAPL', start='2021-01-01', end='2021-12-31')
# 'AAPL' is the ticker symbol for Apple Inc.
data.to_csv('aapl_data.csv')
#  = pd.read_csv('aapl_data.csv')

# Select relevant features (columns) for anomaly detection.
features = ['Close', 'Volume']
X = data[features].values

# Data preprocessing: Standardize the features (mean=0, std=1).
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Create and fit the Isolation Forest model.
model = IsolationForest(contamination=0.05, random_state=42)  # Adjust the contamination parameter as needed.
model.fit(X)

# Predict anomalies (1 for normal, -1 for anomalies).
predictions = model.predict(X)

# Add the predictions as a new column in the DataFrame.
data['Anomaly'] = predictions

# Filter out anomalies.
anomalies = data[data['Anomaly'] == -1]

# Display or save the detected anomalies.
print("Detected Anomalies:")
print(anomalies)

# Visualize the financial data with anomalies highlighted.
plt.figure(figsize=(12, 6))
plt.scatter(data.index, data['Close'], c=predictions, cmap='viridis', marker='o')
plt.xlabel('Time Index')
plt.ylabel('Close Price')
plt.title('Financial Market Data with Anomalies Highlighted')
plt.colorbar(label='Anomaly (1=Normal, -1=Anomaly)')
plt.show()

# Evaluation (optional): You can evaluate the model's performance using classification metrics such as precision, recall, and F1-score.
from sklearn.metrics import classification_report
true_labels = np.where(data['Anomaly'] == -1, 1, 0)
print("Classification Report:")
print(classification_report(true_labels, predictions))

# Optionally, you can save the detected anomalies to a CSV file or further analyze them.
anomalies.to_csv('detected_anomalies.csv', index=False)
