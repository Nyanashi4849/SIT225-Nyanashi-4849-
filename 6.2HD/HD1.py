# This script creates an interactive dashboard using Streamlit to visualize sensor data from a CSV file.
# improting necessary libraries
# Streamlit is a popular library for creating web applications for data science and machine learning projects.
import streamlit as st
# pandas is used data manipulation and analysis library.
import pandas as pd
# matplotlib is used for creating static, animated, and interactive visualizations in Python.
import matplotlib.pyplot as plt
# seaborn  that provides a high-level interface for making graphics.
import seaborn as sns
# os  provides functions for interacting with the operating system.
import os
# time provides various time-related functions.
import time

# Function to load data
# This function reads a CSV file containing sensor data and returns a DataFrame.
@st.cache_data
def load_data():
# The CSV file is expected to have a header row with the following columns: timestamp, x, y, z.
    df = pd.read_csv("5.2D.csv", names=["timestamp", "x", "y", "z"])
    
    # Ensure timestamp is converted correctly to datetime format.
    # This is crucial for time stamp data visualization.
    try: 
        df["timestamp"] = pd.to_datetime(df["timestamp"])
    except Exception:
        df["timestamp"] = pd.to_numeric(df["timestamp"], errors='coerce')


    return df

# Load dataset 
df = load_data()

# Set the title of the page
st.title("Interactive Sensor Data Dashboard")

# Set the title of the sidebar where the user can select options
st.sidebar.header("Visualization Settings")

# Graph Type Selection like Line Chart, Scatter Plot, Distribution Plot
# The user can select the type of graph they want to visualize.
graph_type = st.sidebar.selectbox("Select Graph Type", ["Line Chart", "Scatter Plot", "Distribution Plot"])

# Select Data Variables like x, y, z
# The user can select which data variables they want to visualize.
selected_vars = st.sidebar.multiselect("Select Data Variables", ["x", "y", "z"], default=["x", "y", "z"])

# User input for number of data samples to display 
num_samples = st.sidebar.number_input("Enter number of samples to display", min_value=1, max_value=len(df), value=10, step=1)

# Navigation buttons for previous and next samples
# These buttons allow the user to move back and forth through the data samples.
if "start_index" not in st.session_state:
    st.session_state.start_index = 0

# Buttons for navigating through the data samples.
prev_button = st.sidebar.button("Previous")
next_button = st.sidebar.button("Next")

# Button to reset the index to the first sample.
if prev_button:
    st.session_state.start_index = max(0, st.session_state.start_index - num_samples)

if next_button:
    st.session_state.start_index = min(len(df) - num_samples, st.session_state.start_index + num_samples)

# Filter data for display based on the selected number of samples.
df_display = df.iloc[st.session_state.start_index : st.session_state.start_index + num_samples]

#  sets subheader - data summary
st.subheader(" Data Summary")
st.write(df_display.describe())

# sets subheader - graphname visuallisation
st.subheader(f" {graph_type} Visualization")

# Create a figure for the selected graph type
fig, ax = plt.subplots(figsize=(10, 5))

# Plotting based on the selected graph type
# The graph type is determined by the user's selection in the sidebar.
#  if loop for line chart which sets the x and y axis values. 
if graph_type == "Line Chart":
    for var in selected_vars:
        ax.plot(df_display["timestamp"], df_display[var], label=f"{var}-axis")

        #  x axis is set to timestamp and y axis is set to sensor values.
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Sensor Values")

    #   legend is set to show the variable names.
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

# elif graph_type == "SCATTER PLOT":
elif graph_type == "Scatter Plot":
    for var in selected_vars:
        ax.scatter(df_display["timestamp"], df_display[var], label=f"{var}-axis", alpha=0.7)

     #  x axis is set to timestamp and y axis is set to sensor values.
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Sensor Values")

    #   legend is set to show the variable names.
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

# elif graph_type == "Histogram":
elif graph_type == "Distribution Plot":
    if selected_vars:
        for var in selected_vars:
            sns.histplot(df_display[var], kde=True, label=f"{var}-axis", alpha=0.6)

            #  x axis is set to sensor values and y axis is set to timestamp.
        plt.xlabel("Sensor Values")
        plt.legend()
        st.pyplot(plt)

        # if user does not select any variable, it will show a warning message.
    else:
        st.warning("Please select at least one variable to display the distribution plot.")

# Continuous Sensor Data Update 
# This section allows the user to enable auto-refresh for the data visualization.

#  sets subheader - auto-update settings
st.sidebar.subheader(" Auto-Update Settings")
auto_refresh = st.sidebar.checkbox("Enable Auto-Refresh", value=False)

#  if user selects auto-refresh, it will show a slider to select the refresh interval.
if auto_refresh:
    refresh_interval = st.sidebar.slider("Select Refresh Interval (seconds)", 5, 30, 10)
    
    # This loop will keep refreshing the data at the specified interval.
    while auto_refresh:
        # Simulating new data file after 10s
        time.sleep(refresh_interval)
        
        # Reload data (simulate new file)
        df = load_data()
        
        # Update displayed data
        df_display = df.iloc[st.session_state.start_index : st.session_state.start_index + num_samples]
        st.experimental_rerun()