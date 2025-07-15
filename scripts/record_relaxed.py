import serial
import time
import csv

# === CONFIGURATION ===
PORT = 'COM7'  # Replace with your actual port (e.g., COM4, COM5, etc.)
BAUD_RATE = 9600
DURATION = 30  # Duration to record (in seconds)
FILENAME = 'relaxed_data.csv'

# === CONNECT TO ARDUINO ===
print(f"Connecting to {PORT}...")
ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # Wait for Arduino to reset

print("Connected! Starting to read data...")

# === PREPARE TO WRITE CSV ===
with open(FILENAME, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['timestamp', 'value'])  # Write header

    start_time = time.time()
    while time.time() - start_time < DURATION:
        line = ser.readline().decode('utf-8').strip()
        if line.isdigit():
            value = int(line)
            timestamp = time.time() - start_time
            writer.writerow([timestamp, value])
            print(f"{timestamp:.2f}s → {value}")

print(f"Finished! Data saved to '{FILENAME}'.")
ser.close()