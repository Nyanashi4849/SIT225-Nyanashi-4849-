# Import necessary libraries
import sys
import time
import traceback
import os
# For Arduino IoT Cloud communication
from arduino_iot_cloud import ArduinoCloudClient  
import csv
# For data handling
import pandas as pd  
# For plotting
import plotly.express as px  
# To save plots as images
import plotly.io as pio  
 # For visualization
import seaborn as sns 
# Traditional plotting
import matplotlib.pyplot as plt  

# Arduino Cloud device credentials
DEVICE_ID = "d292d609-626a-4200-809c-fc67df5ab96a"
SECRET_KEY = "mF0Fef8w14qNRB1tsB3YRPGtt"

# Variables to store accelerometer readings
cur_data = []  # Latest data
temp_data = []  # Temporary data to batch store readings
x, y, z = 0, 0, 0  # Current accelerometer values
count = 0  # Counter for number of samples collected
N_SAMPLES = 20  # Number of samples to collect before saving

# =============================================================================
# Callback function when accelerometer X value changes
def on_accelerometer_x_changed(client, value):
    global x
    x = value  # Update global x value

# Callback function when accelerometer Y value changes
def on_accelerometer_y_changed(client, value):
    global y
    y = value  # Update global y value

# Callback function when accelerometer Z value changes
def on_accelerometer_z_changed(client, value):
    global z
    z = value  # Update global z value

#================================= MAIN FUNCTION =================================
if __name__ == "__main__":
    try:
        # Create Arduino Cloud client instance
        client = ArduinoCloudClient(
            device_id=DEVICE_ID, 
            username=DEVICE_ID, 
            password=SECRET_KEY, 
            sync_mode=True
        )

        # Register the callback functions for accelerometer values
        client.register("py_x", value=None, on_write=on_accelerometer_x_changed)
        client.register("py_y", value=None, on_write=on_accelerometer_y_changed)
        client.register("py_z", value=None, on_write=on_accelerometer_z_changed)

        client.start()  # Start communication with Arduino IoT Cloud

        # Continuously collect and process data
        while True:
            if x is not None and y is not None and z is not None:
                if count < N_SAMPLES:
                    # Collect sample
                    count += 1
                    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                    temp_data.append([count, timestamp, x, y, z])
                    print([count, timestamp, x, y, z])
                    # Reset x, y, z to avoid duplicate readings
                    x, y, z = None, None, None
                else:
                    # Save data to CSV once enough samples are collected
                    timestamp = time.strftime('%Y-%m-%d_%H-%M-%S')
                    df = pd.DataFrame(temp_data, columns=['index', 'Timestamp', 'X', 'Y', 'Z'])
                    df.to_csv(f"csv_{timestamp}.csv")

                    # Plot the collected data
                    fig = px.line(df, x='Timestamp', y=['X', 'Y', 'Z'])
                    filename = f"images/plot_{timestamp}.png"  # Save plot image
                    pio.write_image(fig, filename)

                    # Reset counter and move temp_data to cur_data
                    count = 0
                    cur_data = temp_data.copy()
                    temp_data.clear()
            client.update()  # Maintain connection with cloud

    except:
        # Error handling block
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_tb(exc_type, file=print)  # Print stack trace

        # If an error happens, run a Dash server for visualization
        app.run_server(debug_mode=True, jupyter_tab=True)

        # Load a different CSV for analysis
        _df = pd.read_csv("811P.csv")
        _df.drop(columns={"Unnamed: 0", "index"}, inplace=True)  # Drop unnecessary columns
        _df.Timestamp = pd.to_datetime(_df.Timestamp)  # Convert to datetime
        _df.set_index("Timestamp", inplace=True)  # Set timestamp as index

        # Segment the dataset into 5 activities based on time intervals
        act_1 = _df.between_time("01:15:40", "01:16:30")
        act_2 = _df.between_time("01:16:50", "01:18:30")
        act_3 = _df.between_time("01:21:10", "01:22:40")
        act_4 = _df.between_time("01:24:45", "01:25:15")
        act_5 = _df.between_time("01:30:00", "01:30:40")

        act_1.info()  # Show information about activity 1 data

        # Plotting full dataset for X, Y, and Z
        figsize = (16, 9)
        sns.lineplot(x=_df.index, y=_df["X"], label="X")
        sns.lineplot(x=_df.index, y=_df["Y"], label="Y")
        sns.lineplot(x=_df.index, y=-_df["Z"], label="Z")  # Notice '-' sign for Z

        # Create separate plots for each activity
        fig, ax = plt.subplots(5, figsize=(10, 9))

        for i, data in enumerate([act_1, act_2, act_3, act_4, act_5]):
            sns.lineplot(x=data.index, y=data["X"], label="X", ax=ax[i])
            sns.lineplot(x=data.index, y=data["Y"], label="Y", ax=ax[i])
            sns.lineplot(x=data.index, y=data["Z"], label="Z", ax=ax[i])
            ax[i].legend()

        plt.tight_layout()  # Adjust layout to avoid overlapping
        plt.show()  # Display plots

        # Display statistical summary of activities
        act_1.describe()
        act_2.describe()
