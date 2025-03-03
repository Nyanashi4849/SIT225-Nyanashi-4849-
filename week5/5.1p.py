import serial
import json
import time
import firebase_admin
from firebase_admin import credentials, db
import pandas as pd
import matplotlib

matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt

databaseURL = 'https://week5-ed6e4-default-rtdb.firebaseio.com/'
cred_obj = firebase_admin.credentials.Certificate(
    'week5-ed6e4-firebase-adminsdk-fbsvc-e46ab58d04.json'
)
default_app = firebase_admin.initialize_app(cred_obj, {
	'databaseURL':databaseURL
	})

# Opening serial connection
ser = serial.Serial('COM8', 115200) 

# Firebase reference
ref = db.reference("gyroscope_data")

# CSV file setup
csv_filename = "5.1.csv"
with open(csv_filename, "w") as f:
    f.write("timestamp,x,y,z\n")

try:
    while True:
        line = ser.readline().decode().strip()
        if line:
            parts = line.split(",")
            timestamp, x, y, z = parts[0], float(parts[1]), float(parts[2]), float(parts[3])

            # Create JSON data
            data = {"timestamp": timestamp, "x": x, "y": y, "z": z}
            ref.push(data)  # Upload to Firebase
            
            # Append to CSV
            with open(csv_filename, "a") as f:
                f.write(f"{timestamp},{x},{y},{z}\n")

            print(f"Data: {data}")

except KeyboardInterrupt:
    print("Data collection stopped.")
    ser.close()

data = ref.get()

# Converting Data to CSV
df = pd.DataFrame(data.values())  
df.to_csv("5.1.csv", index=False)

# Ploting Graphs
plt.figure(figsize=(10, 5))
plt.plot(df["timestamp"], df["x"], label="X-axis")
plt.plot(df["timestamp"], df["y"], label="Y-axis")
plt.plot(df["timestamp"], df["z"], label="Z-axis")
plt.legend()
plt.title("Gyroscope Data Over Time")
plt.savefig("gyro_plot1.png")

df = pd.read_csv("5.1.csv")
df = df.dropna()  # Remove empty fields
df = df[df.applymap(lambda x: isinstance(x, (int, float))).all(1)]  # Keep only numeric values
df.to_csv("5.1.csv", index=False)
print("Data cleaned and saved!")

# Read data
df = pd.read_csv("5.1.csv")

# Plot x, y, z separately
plt.figure(figsize=(10, 6))

plt.subplot(3, 1, 1)
plt.plot(df["timestamp"], df["x"], label="X-axis", color="red")
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(df["timestamp"], df["y"], label="Y-axis", color="green")
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(df["timestamp"], df["z"], label="Z-axis", color="blue")
plt.legend()

plt.tight_layout()
plt.savefig("gyro_plots1.png")
# plt.show()

# Combined plot
plt.figure(figsize=(10, 4))
plt.plot(df["timestamp"], df["x"], label="X", color="red")
plt.plot(df["timestamp"], df["y"], label="Y", color="green")
plt.plot(df["timestamp"], df["z"], label="Z", color="blue")
plt.legend()
plt.savefig("combined_plot1.png")
# plt.show()
