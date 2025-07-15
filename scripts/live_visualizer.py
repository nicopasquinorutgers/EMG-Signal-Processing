import serial
import time
import joblib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

# === CONFIGURATION ===
PORT = 'COM7'  # Update to match your Arduino port
BAUD_RATE = 9600
MODEL_PATH = 'model_raw.pkl'
WINDOW_SIZE = 100  # number of recent points to show on plot
SMOOTHING = 5  # number of points to average

# === Load model ===
model = joblib.load(MODEL_PATH)
print("Model loaded")

# === Connect to Arduino ===
ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
time.sleep(2)
print("Connected to Arduino")

# === Buffers ===
raw_buffer = deque(maxlen=WINDOW_SIZE)
smoothed_buffer = deque(maxlen=SMOOTHING)

# === Set up plot ===
plt.style.use('ggplot')
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
text_label = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=14,
                     bbox=dict(facecolor='white', edgecolor='black'))

def init():
    ax.set_xlim(0, WINDOW_SIZE)
    ax.set_ylim(0, 1100)  # potentiometer values range from 0 to 1023
    line.set_data([], [])
    text_label.set_text('')
    return line, text_label

def update(frame):
    line_data = []

    while ser.in_waiting:
        try:
            line_in = ser.readline().decode('utf-8').strip()
            if line_in.isdigit():
                value = int(line_in)
                smoothed_buffer.append(value)
                smoothed = int(sum(smoothed_buffer) / len(smoothed_buffer))
                prediction = model.predict([[int(smoothed)]])[0]
                print(f"🔢 Smoothed: {smoothed}, Prediction: {prediction}")

                raw_buffer.append(smoothed)
                line_data = list(raw_buffer)

                line.set_data(range(len(line_data)), line_data)
                text_label.set_text(f'Prediction: {prediction}')
        except:
            pass

    return line, text_label

ani = animation.FuncAnimation(fig, update, init_func=init, blit=True, interval=100)
plt.title("Live EMG Simulation Signal + Prediction")
plt.xlabel("Time (Recent Samples)")
plt.ylabel("Analog Value")
plt.tight_layout()
plt.show()

ser.close()
