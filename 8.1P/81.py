# Importing required libraries - for connecting to Arduino IoT Cloud, Plotly for interactive plotting, High-level plotly interface,
# pandas For data handling , seaborn For advanced statistical visualization, Dash framework for web app
import sys
import time
import traceback
import os
from arduino_iot_cloud import ArduinoCloudClient 
import csv 
import time
import plotly.io as pio 
import plotly.express as px  
import pandas as pd  
import seaborn as sns  
import dash 
# Dash components
from dash import dcc, html  
# Dash input-output linking
from dash.dependencies import Input, Output  
# More detailed Plotly plotting
import plotly.graph_objs as go  
# For traditional plotting with Matplotlib
import matplotlib.pyplot as plt  

# Reading accelerometer data from CSV files
accelerometer_x = pd.read_csv('8.1Accelerometer_X.csv')
accelerometer_y = pd.read_csv('8.1Accelerometer_Y.csv')
accelerometer_z = pd.read_csv('8.1Accelerometer_Z.csv')

# Converting 'time' columns to datetime format for proper plotting
accelerometer_x.time = pd.to_datetime(accelerometer_x.time)
accelerometer_y.time = pd.to_datetime(accelerometer_y.time)
accelerometer_z.time = pd.to_datetime(accelerometer_z.time)

# Plotting accelerometer data using Matplotlib
plt.figure(figsize=(12, 8))  # Setting figure size

# Plot X-axis accelerometer data
plt.subplot(2, 2, 1)
plt.plot(accelerometer_x['time'], accelerometer_x['value'])
plt.title('Accelerometer X')

# Plot Y-axis accelerometer data
plt.subplot(2, 2, 2)
plt.plot(accelerometer_y['time'], accelerometer_y['value'])
plt.title('Accelerometer Y')

# Plot Z-axis accelerometer data
plt.subplot(2, 2, 3)
plt.plot(accelerometer_z['time'], accelerometer_z['value'])
plt.title('Accelerometer Z')

# Plot all three axes together for comparison
plt.subplot(2, 2, 4)
plt.plot(accelerometer_x['time'], accelerometer_x['value'], label='X')
plt.plot(accelerometer_y['time'], accelerometer_y['value'], label='Y')
plt.plot(accelerometer_z['time'], accelerometer_z['value'], label='Z')
plt.title('Accelerometers X, Y, and Z')

# Adding x and y labels to all subplots
for i in range(3):
    plt.subplot(2,2,i+1)
    plt.xlabel('Time')
    plt.ylabel('Value')

plt.tight_layout()  # Adjust layout to prevent overlap
plt.show()  # Display the plots

# Setting up Dash web application
app = dash.Dash(__name__)

# Define the layout of the app
 # Graph that will be updated live
app.layout = html.Div([
    dcc.Graph(id='live-update-graph'), 
     # Interval triggers every 1 second
    dcc.Interval(id='interval-component', interval=1000, n_intervals=0) 
])

# Callback function to update the graph periodically
 # Output: Figure of the graph
@app.callback(
    Output('live-update-graph', 'figure'),  
    # Input: Number of intervals passed
    Input('interval-component', 'n_intervals')  
)
def update_graph(n_intervals):
    global cur_data
    # Convert the current accelerometer data into a pandas DataFrame
    df = pd.DataFrame(cur_data, columns=['index','Timestamp', 'X', 'Y', 'Z'])
    # Create a line plot using Plotly Express
    fig = px.line(df, x= 'Timestamp', y = ['X','Y','Z'])  # Plotting X, Y, Z vs Time

    return fig  # Returning the updated figure to the graph
