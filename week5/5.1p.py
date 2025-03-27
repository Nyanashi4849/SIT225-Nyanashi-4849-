 # Import serial communication library, JSON module for handling data, time module for timestamps, Firebase Admin SDK, pandas for data handling, matplotlib for plotting graphs

import serial 
import json  
import time  
import firebase_admin  
from firebase_admin import credentials, db  
import pandas as pd  
import matplotlib  
 # Use non-GUI backend for matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt  # Import pyplot for plotting

# Firebase Database URL
databaseURL = 'https://week5-ed6e4-default-rtdb.firebaseio.com/'

# Load Firebase credentials from JSON file
cred_obj = firebase_admin.credentials.Certificate(
    'week5-ed6e4-firebase-adminsdk-fbsvc-e46ab58d04.json'
)

# Initialize Firebase application with database URL
default_app = firebase_admin.initialize_app(cred_obj, {
    'databaseURL': databaseURL
})

# Open Serial Connection to Arduino
try:
	# Open serial on port COM8
    ser = serial.Serial('COM8', 115200)  
    print("Serial connection established.")
except serial.SerialException as e:
    print(f"Serial connection error: {e}")
    exit()  # Exit if serial connection fails

# Firebase reference to store gyroscope data
ref = db.reference("gyroscope_data")

# CSV file setup for saving the data in csv file
csv_filename = "5.1.csv"
with open(csv_filename, "w") as f:
    f.write("timestamp,x,y,z\n")  # Write CSV header (first line writen in csv file)

try:
    while True:
        # Read data from serial port
        line = ser.readline().decode().strip() 
        if line:
            try:
                # Split incoming data by commas
                parts = line.split(",")
                
                # Extract timestamp and gyroscope values
                timestamp, x, y, z = int(parts[0]), float(parts[1]), float(parts[2]), float(parts[3])

                # Create JSON data object
                data = {"timestamp": timestamp, "x": x, "y": y, "z": z}

                # Upload data to Firebase
                ref.push(data)

                # Append data to CSV file
                with open(csv_filename, "a") as f:
                    f.write(f"{timestamp},{x},{y},{z}\n")

                # Print received data to console
                print(f"Data: {data}")

            except ValueError:
                print(f"Invalid data received: {line}")  # Handle incorrect data format

except KeyboardInterrupt:
    # Stop data collection when user wants
    print("Data collection stopped.")
    ser.close()  # Close serial connection

# get data from Firebase for processing
data = ref.get()

if data:
    # Convert Firebase data to Pandas
    df = pd.DataFrame(data.values())
    df.to_csv(csv_filename, index=False)  # Save DataFrame in CSV file

    # Convert timestamp column to numeric format
    df["timestamp"] = pd.to_numeric(df["timestamp"], errors='coerce')

    # Clean data by removing unneccesary values
    df = df.dropna()

    # Ensure all values are numeric 
    df = df[df.applymap(lambda x: isinstance(x, (int, float))).all(1)]

    # Save cleaned data to CSV
    df.to_csv(csv_filename, index=False)
    print("Data cleaned and saved!")

    # Plot gyroscope data
    plt.figure(figsize=(10, 5))
    plt.plot(df["timestamp"], df["x"], label="X-axis", color="red")
    plt.plot(df["timestamp"], df["y"], label="Y-axis", color="green")
    plt.plot(df["timestamp"], df["z"], label="Z-axis", color="blue")
    plt.legend()
    plt.title("Gyroscope Data Over Time")
    plt.savefig("gyro_plot1.png")  # Save graph as image

    # Generate separate plots for X, Y, Z axes
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
    plt.savefig("gyro_plots1.png")  # Save multiple plots as image

    # Generate combined plot for all axes
    plt.figure(figsize=(10, 4))
    plt.plot(df["timestamp"], df["x"], label="X", color="red")
    plt.plot(df["timestamp"], df["y"], label="Y", color="green")
    plt.plot(df["timestamp"], df["z"], label="Z", color="blue")
    plt.legend()
    plt.savefig("combined_plot1.png")  # Save combined plot

    print("Plots generated and saved!")

else:
    print("No data found in Firebase.")

# Close serial connection if still open
if ser.is_open:
    ser.close()
    print("Serial connection closed.")
