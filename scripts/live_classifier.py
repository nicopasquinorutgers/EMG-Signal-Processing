import serial
import joblib
import time
import csv
from datetime import datetime

# === CONFIGURATION ===
PORT = 'COM7'  # Make sure this matches your Arduino port
BAUD_RATE = 9600
MODEL_PATH = 'model_raw.pkl'
LOG_FILE = 'live_predictions_log.csv'

# === Load model ===
model = joblib.load(MODEL_PATH)
print("Model loaded")

# === Connect to Arduino ===
ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
time.sleep(2)
print("Connected to Arduino")

# === Prepare CSV logging ===
with open(LOG_FILE, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['timestamp', 'value', 'prediction'])

    print("Logging predictions... Press Ctrl+C to stop.\n")

    try:
        while True:
            line = ser.readline().decode('utf-8').strip()
            if line.isdigit():
                value = int(line)
                prediction = model.predict([[value]])[0]
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

                print(f" {timestamp} | Value: {value} → Prediction: {prediction}")
                writer.writerow([timestamp, value, prediction])
    except KeyboardInterrupt:
        print("\n Stopped by user.")
        ser.close()