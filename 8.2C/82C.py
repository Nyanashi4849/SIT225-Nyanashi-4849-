# This script reads accelerometer data from a CSV file, applies a smoothing algorithm, and plots the results.
#  imported libraries like pandas and matplotlib for data manipulation and visualization.
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import pandas as pd


# Load the CSV file. file name is 82C.csv
df = pd.read_csv("82C.csv")

# Convert 'time' to datetime format
df['time'] = pd.to_datetime(df['time'])

# Apply smoothing: 3-point rolling average. This is a simple smoothing technique that averages the current value
df['acc_x_smooth'] = df['acc_x'].rolling(window=3).mean()
df['acc_y_smooth'] = df['acc_y'].rolling(window=3).mean()
df['acc_z_smooth'] = df['acc_z'].rolling(window=3).mean()

# Plot original vs smoothed values
plt.figure(figsize=(14, 6))

# Plot RAW lines. These are the original accelerometer data points. 
plt.plot(df['time'], df['acc_x'], label='acc_x (Raw)', color='red', alpha=0.4, linestyle='--')
plt.plot(df['time'], df['acc_y'], label='acc_y (Raw)', color='green', alpha=0.4, linestyle='--')
plt.plot(df['time'], df['acc_z'], label='acc_z (Raw)', color='blue', alpha=0.4, linestyle='--')

# Plot SMOOTH lines. These are the smoothed accelerometer data points.
# The smoothed data is easier to interpret.
plt.plot(df['time'], df['acc_x_smooth'], label='acc_x (Smooth)', color='red')
plt.plot(df['time'], df['acc_y_smooth'], label='acc_y (Smooth)', color='green')
plt.plot(df['time'], df['acc_z_smooth'], label='acc_z (Smooth)', color='blue')

# Graph styling
# The title for the graph
plt.title("Accelerometer Data: Raw vs Smoothed")
# The x-axis and y-axis labels. x as time and y as acceleration in m/s²
plt.xlabel("Time")
plt.ylabel("Acceleration (m/s²)")
# The legend for the graph. it shows which line corresponds to which data point.
plt.legend()
# Grid lines for better readability. it helps to see the data points more clearly.
plt.grid(True)
# The x-axis ticks are rotated for better readability. it helps to see the time values more clearly.
plt.xticks(rotation=45)
# The y-axis limits are set to -2 and 2. This is to focus on the relevant data points.
plt.tight_layout()
#  The figure is saved as a PNG file. This is to save the graph for later use.
# The file name is smoothed_plot.png.
plt.savefig("smoothed_plot.png")
print("Plot saved as smoothed_plot.png")


