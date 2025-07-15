import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# === CONFIGURATION ===
LOG_FILE = 'live_predictions_log.csv'  # Change if your filename differs

# === Load data ===
df = pd.read_csv(LOG_FILE)
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y-%m-%d %H:%M:%S.%f')

# === Assign colors for prediction labels ===
df['color'] = df['prediction'].map({'relaxed': 'skyblue', 'flexed': 'salmon'})

# === Plot ===
fig, ax = plt.subplots(figsize=(12, 6))
ax.set_title('EMG Signal + Live Predictions')
ax.set_xlabel('Time')
ax.set_ylabel('Analog Value')

# Plot signal line
ax.plot(df['timestamp'], df['value'], label='Signal', color='black', linewidth=1)

# Color segments based on prediction
for i in range(1, len(df)):
    ax.plot(df['timestamp'].iloc[i-1:i+1], df['value'].iloc[i-1:i+1],
            color=df['color'].iloc[i], linewidth=2)

# Format time axis
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S.%f'))
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(True)
plt.legend()
plt.savefig('prediction_plot.png')
plt.show()